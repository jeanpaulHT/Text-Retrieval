
#Variables that contains the user credentials for the Twitter API 
access_token = "1369347540454408197-FXU7wauQT8qJGmWZ6YilJCjWF7IZ07"
access_token_secret = "PTXoqz7ixHPBvYJn0ank5O8IpqHa3bkbyXHs3UmQ0FSL5"
consumer_key = "zjKw6LU9PPXyJrhrHj4Nlr92i"
consumer_secret = "k0f2M8rGHySoUICYDGJfbdwf4hLyvgVL8PlMXtJHk8ACmsdKSC"

#destination folder for raw tweets 
folder_path = "raw/"
#destination folder for clean tweets
clean_path = "clean/"

# the list of tracking words 
"""
tracklist = {
'@luchocastanedap': ['@luchocastanedap', 'luis castañeda',  'Luis Castañeda Pardo'],
'@DanielUrresti1': ['@DanielUrresti1', 'Daniel Urresti'],
'@humberto_lay': ['@humberto_lay', 'Humberto Lay', 'Humberto Lay Sun'],
'@RicardoBelmontC': ['@RicardoBelmontC', 'Ricardo Belmont', 'Ricardo Belmont Cassinelli'],
'@BeingoleaA': ['@BeingoleaA', 'Alberto Beingolea'],
'@jaimesalinas80': ['@jaimesalinas80', 'Jaime Salinas'],
'@JorgeMunozAP': ['@JorgeMunozAP', 'Jorge Muñoz', 'Jorge Muñoz Wells'],
'@EstherCapunay': ['@EstherCapunay', 'Esther Capuñay', 'La Capuñay'],
'@ManuelVelardeD': ['@ManuelVelardeD', 'Manuel Velarde'],
'@DitelColumbus': ['@DitelColumbus', 'Ditel Columbus', 'Ditel Columbus - LIMA'],
'@ENRIQUECORNEJOR': ['@ENRIQUECORNEJOR', 'Enrique Cornejo'],
'@juancarloszurek': ['@juancarloszurek', 'Juan Carlos Zurek'],
'@JulioGagoPe': ['@JulioGagoPe', 'Julio Gagó Pérez', 'Julio Gagó'],
'@Renzo_Reggiardo': ['@Renzo_Reggiardo', 'Renzo Reggiardo'],
'@EnriquePorLima': ['@EnriquePorLima', 'Enrique Fernández Chacón'],
'@kikeocrospoma': ['@kikeocrospoma', 'Enrique Ocrospoma'],
'@GGG_pe': ['@GGG_pe', 'Gustavo Guerra García'],
'@GomezBacaxLima': ['@GomezBacaxLima', 'Roberto Gómez Baca']
}
"""

# tracklist = {
#     'peter castle': ['Pedro Castillo', '@PedroCastilloTe']
#     # 'señora k': ['Keiko Fujimori', '@KeikoFujimori'],
#     # 'Mi Fiscal':['Jose Domingo Perez', '@JoseDomingoPer']
# }
#

tracklist = {
    'covid': ['covid',  'covid-19']
}