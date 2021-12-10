import sys
import zipfile
from zipfile import ZipFile
import os
from datetime import datetime
import time

param = sys.argv[1:]
strCaminho = None
strExtensao = None

if len(param) == 0:
    strCaminho = None
else: 
    strCaminho = param[0]
    strExtensao = param[1]
    strExtensao = strExtensao.upper()

def F_formata_Ano_Mes(p_strVariavel):
    strAno = p_strVariavel[0:4]
    strMes = p_strVariavel[4:6]

    strData = strAno + strMes

    return strData

def F_geraZip(p_strPastaOrigem, p_strNomeArquivo, p_strAnoMesAtual, p_strData,p_extensao):

    #Muda para o diretório onde estão os arquivos.
    os.chdir(p_strPastaOrigem)

    #Pega o mês da última data de modificação do arquivo.
    dataCriacaoArquivo = os.path.getmtime(p_strNomeArquivo)
    intMes = time.ctime(dataCriacaoArquivo)
    objTempo = time.strptime(intMes)
    dataArquivo= time.strftime("%Y%m%d", objTempo)
    strAnoMesArquivo = F_formata_Ano_Mes(dataArquivo)

    strPastaBackup = p_strPastaOrigem + "/BKP_"+p_extensao

    aExtensaoArquivo = os.path.splitext(p_strNomeArquivo)
    strExtensaoArquivo = aExtensaoArquivo[1].upper()
    strExtensaoArquivo = strExtensaoArquivo.replace(".","")

    '''
    Busca o arquivo que termina com uma extensão específica e que possui a data de modificação diferente do mês atual.
    Após pegar o valor do mês do arquivo modificado, armazena numa lista o valor do mês, caso este mesmo
    não esteja já na estrutura de armazenamento.Além disso, também é criado um arquivo .zip e armazenado seu valor numa outra lista,
    para que seja possível comparar as duas listas posteriormente e fazer algumas verificações.
    Se o mês em que o arquivo foi modificado já estiver na lista, busca-se o index dele na estrutura e compara com o index da lista dos arquivos zip,
    e finalmente copia-se o arquivo que está sendo iterado para o ZIP correlato ao index pesquisado.
    '''
    try:
        if strExtensaoArquivo == p_extensao and strAnoMesArquivo != p_strAnoMesAtual:

            if strAnoMesArquivo not in aAnoMes:

                aAnoMes.append(strAnoMesArquivo)

                if not os.path.exists(strPastaBackup):
                    os.makedirs(strPastaBackup)

                arquivoZip = ZipFile(strPastaBackup + "/" + "BKP_" + p_strData + "_" + strAnoMesArquivo+ "_" + p_extensao +".zip", 'w')
                aArquivosZip.append(arquivoZip)
                arquivoZip.write(p_strNomeArquivo)
                os.remove(p_strNomeArquivo)

            else:
                for contador, anoMes in enumerate(aAnoMes):

                    if strAnoMesArquivo == anoMes:

                        intCount = len(aArquivosZip[contador].infolist())
                        if intCount < 1000:

                            aArquivosZip[contador].write(p_strNomeArquivo)
                            os.remove(p_strNomeArquivo)

    except(Exception, zipfile.BadZipfile) as e:
        print("Erro Inesperado:", sys.exc_info()[1])

aAnoMes = []
aArquivosZip = []

dataAtual = datetime.now().strftime("%Y%m%d%H%M%S")
strAnoMesAtual = F_formata_Ano_Mes(dataAtual)

for strNomeArquivo in os.listdir(strCaminho):
    F_geraZip(strCaminho, strNomeArquivo, strAnoMesAtual, dataAtual, strExtensao)