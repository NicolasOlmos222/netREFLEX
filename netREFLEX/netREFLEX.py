import reflex as rx
from netREFLEX import style
import pandas as pd
import datetime
#GENERA EL ARCHIVO EXCEL CON LA FECHA ACTUAL
current_datetime = datetime.datetime.now()
archivo = str(current_datetime.strftime("%Y-%m-%d")) + ".xlsx"

class MyState(rx.State):
    cargaDisplay: str = "none"
    docente: str = ""
    curso: str = ""
    
    #DATA: MUESTRA EN INDEX, DATAM: REFERENCIA, DATAG: EXCEL
    data: list = []
    data2: list = []
    dataM: list = []
    dataG:list = []
    columns: list[str] = ["RACK 1", "RACK 2", "RACK 3"]
    
    #NUMERO DE MAQUINA
    numero:str = ""
    
    #GENERA LA TABLA~~~~~~~~~~~~~~~
    for fila in range(30):
        fila_numeros = []
        for columna in range(3):
            fila_numeros.append(0)
        data.append(fila_numeros)
        data2.append(fila_numeros)
        dataG.append(fila_numeros)
        dataM.append(fila_numeros)
    cont = 1
    for i in range(3):
        for k in range(30):
            if cont < 11:
                data[k][i] = "Lenovo'"  + str(cont)
                data2[k][i] = "Lenovo'" + str(cont)
                dataM[k][i] = "Lenovo'" + str(cont)
                dataG[k][i] = "Lenovo'" + str(cont)
            elif cont <43:
                data[k][i] = "LenovoV330'"  + str(cont)
                data2[k][i] = "LenovoV330'" + str(cont)
                dataM[k][i] = "LenovoV330'" + str(cont)
                dataG[k][i] = "LenovoV330'" + str(cont)
            cont += 1
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def setDocente(self,docente: str):
        self.docente = docente
        
    def setCurso(self, curso: str):
        self.curso = curso
    
    def setNumero(self, numero: str):
        self.numero = numero
    
    
        
    def inicioBlock(self):
        if self.cargaDisplay == "none":
            if self.docente != "":
                self.cargaDisplay = "block"
        else:
            self.cargaDisplay = "none"
    
    def ingresar(self):
        for i in range(3):
            for k in range(30):
                #BUSCA LA UBICACION DEL NUMERO "LenovoV330'15" str(self.dataM[k][i])
                if self.dataM[k][i] == self.numero:
                    #ACTUALIZA LA HORA
                    current_datetime = datetime.datetime.now()
                    formatted_datetime = current_datetime.strftime("%H:%M")
                    
                    #CONSULTA SI ESTA YA RESERVADA
                    if self.docente.upper() in self.data[k][i]:
                        self.data[k][i] = self.data2[k][i]
                    else:
                        #REEMPLAZA EN EL CASO QUE NO ESTE RESERVADA Y GUARDA EL HISTORIAL GLOBAL EN EXCEL
                        self.data[k][i] = f"{self.data2[k][i]} ~ Docente: {self.docente.upper()}  Curso: {self.curso.upper()}  Hora: {formatted_datetime} ~"
                        self.dataG[k][i] = self.dataG[k][i] + f" ~ Docente: {self.docente.upper()}  Curso: {self.curso.upper()}  Hora: {formatted_datetime} ~"
                        df = pd.DataFrame(self.dataG, columns=["RACK 1", "RACK 2", "RACK 3"])
                        df.to_excel(archivo, index=True) 
                        
                    #break
        #self.numero = ""
                
                    

#data.at[0, 'Columna1'] = "NICO"

@rx.page(route="/", title="CONTROL PROA") 
def index() -> rx.Component:
    return rx.vstack(
        
        rx.hstack(
            rx.input(
                placeholder="Nombre del docente",
                value=MyState.docente,
                on_change = MyState.setDocente,
                style = style.input_style,
                id="top"
            ),
            rx.input(
                placeholder="Curso",
                value=MyState.curso,
                on_change = MyState.setCurso,
                style = style.input_style,
            ), 
            rx.button(
                "INICIO",
                style = style.boton_style,
                on_click = MyState.inicioBlock(),
            ),   
        ),
        rx.box(
            rx.input(
                placeholder="Escanear netbook",
                autofocus=True,
                value=MyState.numero,
                on_change = MyState.setNumero,
                on_key_down = MyState.ingresar(),
            ),
            display=MyState.cargaDisplay,
        ),
        rx.data_table(
            data=MyState.data,
            columns=MyState.columns,
        ),
        rx.link("SUBIR", href="",
                bg="lightblue",
                color="black",
                padding="4px",
                border_radius="1em",
                border_width="2px",
                _hover={
                    "bg": "darkblue",
                    "color": "white",
                }
        )
    )
    
# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.compile()
