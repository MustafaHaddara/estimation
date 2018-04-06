def jsonToCard(jsonCard):
    return ( jsonCard['value'], jsonCard['suit'] )

def cardToJson(card):
    return {
        'suit' : card[1],
        'value': card[0]
    }
