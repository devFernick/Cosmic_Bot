import requests
from datetime import datetime

def Post(api):
    print("Se empieza la funcion de nasaAPI.py: Post(api)")
    # Si no es el primer dia del mes no hace nada
    day_of_month = datetime.today().day
    if day_of_month != 1:
        print("Hoy no es el primero del mes. No se publicó el estado de los astronautas.")
        return None

    try:
        astro= requests.get("http://api.open-notify.org/astros.json")
        if(astro.status_code == 200 and astro.json()["message"] == "success"):
            count = astro.json()["number"]
            if(count > 0):
                Crafts = []
                Estado = "At the moment, there are " + str(count) + " astronauts in space! "
                for i in astro.json()["people"]:
                    if(count > 0):
                        Estado = Estado + i["name"]
                        Crafts.append(i["craft"])
                        count = count - 1
                        if(count == 1):
                            Estado = Estado + " and "
                        elif(count > 1):
                            Estado = Estado + ", "
                        elif(count == 0):
                            Estado = Estado + "."

                #Elimina los duplicados en la lista de naves.
                Crafts = list(dict.fromkeys(Crafts)) 
                Hashtags = ""
                for Craft in Crafts:
                    Hashtags= Hashtags + " #" + Craft
                    
                api.update_status(Estado + " #Astronomy #Space" + Hashtags)
                print("Se publicó el estado con los astronautas actuales en el espacio.")
            else:
                api.update_status("At the moment, there are no astronauts in space. #Astronomy #Space")
                print("Se publicó el estado con los astronautas actuales en el espacio.")
    except:
        print("Hubo un error en el fetch o publicación de los astronautas. No se publicó el estado de los astronautas.")
    print("Se termina la funcion de nasaAPI.py: Post(api)")
    return None