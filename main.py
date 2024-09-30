from fastapi import Body, FastAPI, HTTPException, status

app = FastAPI()

prefix = '/hotels'

hotels = [
    {'id': 1, 'title': 'Dubai', 'name': 'dubai'},
    {'id': 2, 'title': 'Sochi', 'name': 'sochi'}
]

@app.get('/hotels')
async def get_hotels():
    return hotels


@app.post('/hotels')
async def create_hotel(name =  Body(str), title = Body(str)):
    global hotels
    new_hotel_id = max(hotel['id'] for hotel in hotels) + 1
    hotels.append({'id': new_hotel_id, 'name': name, 'title': title})
    return hotels[new_hotel_id]


@app.delete('/hotels/{hotel_id}')
async def delete_hotel(hotel_id: int):
    global hotels

    if hotels[hotel_id - 1] in hotels:
        del hotels[hotel_id - 1]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='hotel doesnt exist'
        )
    
    return {'status': status.HTTP_200_OK}



@app.put('/hotels/{hotel_id}')
async def update_hotel(hotel_id: int, name: str = Body(...), title: str = Body(...)):
    global hotels

    if hotels[hotel_id - 1] not in hotels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='hotel doesnt exist')
    
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = title
            hotel['name'] = name 
    
    return hotel



@app.patch('/hotels/{hotel_id}')
async def partial_update_hotel(hotel_id: int, name: str = Body(default=None), title: str = Body(default=None)):
    global hotels

    if hotels[hotel_id - 1] not in hotels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='hotel doesnt exist')

    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = title if title is not None else hotel['title']
            hotel['name'] = name if name is not None else hotel['name']

    return hotel