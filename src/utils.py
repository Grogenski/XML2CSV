from nfelib.v4_00 import leiauteNFe_sub as parser
from lxml import etree
import pandas as pd

class CSVReader:
    '''
    Retorna a taxa % do IBS ou do CBS de acordo com o NCM do produto, condizente com a legislação atual.
    '''
    def __init__(self, ncmNumber):
        '''
        :param ncmNumber: int
        '''
        self.ncmNumber = ncmNumber

    def NCM_ibs(self):
        '''
        Retorna a taxa % do IBS de acordo com o NCM do produto, condizente com a legislação atual.

        :return: float
        '''
        nNCM = self.ncmNumber

        df_NCM = pd.read_csv("database/NCM.csv")
        row_num = df_NCM[df_NCM['Codigo'] == nNCM].index
        IBS = df_NCM.at[row_num[0], "IBS"]

        return IBS

    def NCM_cbs(self):
        '''
        Retorna a taxa % do CBS de acordo com o NCM do produto, condizente com a legislação atual.

        :return: float
        '''
        nNCM = self.ncmNumber

        df_NCM = pd.read_csv("database/NCM.csv")
        row_num = df_NCM[df_NCM['Codigo'] == nNCM].index
        CBS = df_NCM.at[row_num[0], "CBS"]

        return CBS


class TaxCalculator:
    '''
    Retorna o valor calculado dos impostos IBS, CBS e/ou IVA, de acordo com o NCM do produto,
    condizente com a legislação atual, e do valor do produto.

    '''
    def __init__(self, NCM, vProd):
        '''

        :param NCM: int
        :param vProd: float
        '''
        self.NCM = NCM
        self.vProd = vProd

        self.ncm_ = CSVReader(self.NCM)


    def IBScalc(self):
        '''
        Retorna o cálculo do IBS, considerando o valor e o tipo do produto.

        :return: float
        '''
        vProd = self.vProd
        ncm_ = self.ncm_

        taxIBS = ncm_.NCM_ibs()

        ibs = vProd * taxIBS

        return ibs


    def CBScalc(self):
        '''
        Retorna o cálculo do CBS, considerando o valor e o tipo do produto.

        :return: float
        '''
        vProd = self.vProd
        ncm_ = self.ncm_

        taxCBS = ncm_.NCM_cbs()

        cbs = vProd * taxCBS

        return cbs


    def IVAcalc(self):
        '''
        Retorna o cálculo do IVA, considerando o valor e o tipo do produto.

        :return: float
        '''
        vProd = self.vProd
        ncm_ = self.ncm_

        ibs = ncm_.NCM_ibs()
        cbs = ncm_.NCM_cbs()

        iva = ibs + cbs

        return iva


class NFExtractor:
    '''
    Retorna um DataFrame com informações pertinentes da NFe (.xml) processada. Durante o processo, para cada
    grupo de campos, foram criados dicionários para serem armazenados as informações contidas nos campos. Ao
    final do processo, os dicionários foram convertidos em um único DataFrame.

        dict_ide ->                         INFORMAÇÕES DE IDENTIFICAÇÃO DA NF-E
            "NFe_ID":                       Chave de acesso da NFe, contém 44 caracteres numéricos que servem para representar unicamente um documento fiscal eletrônico.
        dict_emit ->                        IDENTIFICAÇÃO DO EMITENTE DA NOTA FISCAL ELETRÔNICA
            "CNPJ":                         CNPJ do emitente
            "xNome":                        Razão Social ou Nome   do emitente
            "xFant":                        Nome fantasia
            "cMun":                         Código do município
            "xMun":                         Nome do município
            "UF":                           Sigla da UF
            "CEP":                          Código do CEP
            "cPais":                        Código do País
            "xPais":                        Nome do País
        dict_dest ->                        IDENTIFICAÇÃO DO DESTINATÁRIO DA NOTA FISCAL ELETRÔNICA
            "CNPJ":                         CNPJ do destinatário
            "xNome":                        Razão Social ou nome do destinatário
            "cMun":                         Código do município do destinatário
            "xMun":                         Nome do município do destinatário
            "UF":                           Sigla da UF do destinatário
            "CEP":                          Código do CEP do destinatário
            "cPais":                        Código do País do destinatário
            "xPais":                        Nome do País do destinatário
        dict_infNFe ->                      INFORMAÇÕES DE IDENTIFICAÇÃO DA NF-E POR PRODUTO OU SERVIÇO
            "chNFe":                        Chave de acesso da NFe por produto ou serviço
        dict_det ->                         DETALHAMENTO DE PRODUTOS E SERVIÇOS DA NF-E
            "nItem":                        Número do produto ou serviço
            "cProd":                        Código do produto ou   serviço
            "cEAN":                         GTIN (Global Trade   Item Number) do produto, antigo código EAN ou código de barras
            "xProd":                        Descrição do produto   ou serviço
            "NCM":                          Código NCM com 8   dígitos ou 2 dígitos (gênero)
            "uCom":                         Unidade Comercial
            "qCom":                         Quantidade Comercial
            "vUnCom":                       Valor Unitário de   comercialização
            "vProd":                        Valor Total Bruto dos   Produtos ou Serviços
            "uTrib":                        Unidade Tributável
            "qTrib":                        Quantidade Tributável
            "vUnTrib":                      Valor Unitário de   tributação
            "indTot":                       Indica se valor do   Item (vProd) entra no valor total da NF-e (vProd)
            ->                              TRIBUTOS INCIDENTES NO PRODUTO OU SERVIÇO
            "vTotTrib":                     Valor aproximado   total por item de tributos federais, estaduais e municipais.
            "det_icms_identity":            TAG de grupo do ICMS   da Operação própria e ST
            "det_icms_orig":                Origem da mercadoria
            "det_icms_CST":                 Tributação do ICMS
            "det_icms_vBCSTRet":            Valor da BC do ICMS ST retido
            "det_icms_pST":                 Alíquota suportada   pelo Consumidor Final
            "det_icms_modBC":               Modalidade de   determinação da BC do ICMS
            "det_icms_vBC":                 Valor da BC do ICMS
            "det_icms_pICMS":               Alíquota do Imposto
            "det_icms_vICMS":               Valor do ICMS
            "det_icms_modBCST":             Modalidade de   determinação da BC do ICMS ST
            "det_icms_pMVAST":              Percentual da margem   de valor Adicionado do ICMS ST
            "det_icms_vBCST":               Valor da BC do ICMS   ST
            "det_icms_pICMSST":             Alíquota do imposto   do ICMS ST
            "det_icms_vICMSST":             Valor do ICMS ST
            "det_icms_vICMSSubstituto":     Valor do ICMS próprio   do Substituto
            "det_icms_vICMSSTRet":          Valor do ICMS ST   retido
            "cEnq":                         Código de   Enquadramento Legal do IPI
            "IPINT": 	                    TAG de grupo do IPI
            "PISNT":                        TAG de grupo do PIS
            "COFINSNT": 	                TAG de grupo do   COFINS
            "PISAliq_CST":                  Código de Situação   Tributária do PIS
            "PISAliq_vBC":                  Valor da Base de   Cálculo do PIS
            "PISAliq_pPIS": 	            Alíquota do PIS (em   percentual)
            "PISAliq_vPIS":                 Valor do PIS
            "COFINSAliq":                   Alíquota do COFINS   (em reais)
            "COFINSAliq_CST":               Código de Situação   Tributária do COFINS
            "COFINSAliq_vBC":               Valor da Base de   Cálculo da COFINS
            "COFINSAliq_pCOFINS":           Alíquota da COFINS   (em percentual)
            "COFINSAliq_vCOFINS":           Valor do COFINS
            "infAdProd":                    Informações   Adicionais do Produto
            "IBS":                          Valor do IBS (Nova Reforma Tributária)
            "CBS":                          Valor do CBS (Nova Reforma Tributária)
            "IVA":                          Valor do IVA (Nova Reforma Tributária)
            "TaxTotalRT":                   Valor total da soma dos impostos
            "ValorTotalRT":                 Valor do produto com a adição dos impostos da Nova Reforma Tributária
        dict_total ->                       VALORES TOTAIS DA NF-E
            "vBC": 	                        Valor Total da BC do ICMS
            "vICMS":                        Valor Total do ICMS
            "vICMSDeson":                   Valor Total do ICMS   desonerado
            "vFCPUFDest":                   Valor Total do ICMS   relativo ao Fundo de Combate à Pobreza (FCP) da UF de destino
            "vICMSUFDest":                  Valor Total do ICMS de   partilha para a UF do destinatário
            "vICMSUFRemet":                 Valor Total do ICMS de   partilha para a UF do remetente
            "vFCP":                         Valor Total do Fundo de   Combate à Pobreza (FCP)
            "vBCST":                        Valor Total da BC do ICMS   ST
            "vST":                          Valor Total do ICMS   ST
            "vFCPST":                       Valor Total do FCP   (Fundo de Combate à Pobreza) retido por substituição tributária
            "vFCPSTRet":                    Valor Total do FCP   (Fundo de Combate à Pobreza) retido anteriormente por substituição tributária
            "vProd":                        Valor Total Bruto dos   Produtos ou Serviços
            "vFrete":                       Valor Total do Frete
            "vSeg": 	                    Valor Total do Seguro
            "vDesc":                        Valor do Desconto
            "vII":                          Valor Total do II
            "vIPI": 	                    Valor Total do IPI
            "vIPIDevol":                    Valor Total do IPI   devolvido
            "vPIS":                         Valor Total do PIS
            "vCOFINS":                      Valor Total do CONFINS
            "vOutro": 	                    Outras Despesas   acessórias
            "vNF": 	                        Valor Total da NF-e
            "vTotTrib":                     Valor aproximado   total de tributos federais, estaduais e municipais.

    :param Arquivo: str
    '''
    def __init__(self, Arquivo):
        '''

        :param Arquivo: str
        '''
        self.Arquivo = Arquivo
        self.dataframe = None

    def NfeID(self):
        '''
        Retorna o ID da NFe processada.

        :param Arquivo: str
        :return: str
        '''
        Arquivo = self.Arquivo
        nota = parser.parse(Arquivo, silence=True)

        Arquivo.replace("nfe/", "")

        nfeid = nota.infNFe.Id
        return nfeid

    def NfeInfo(self):
        '''
        Retorna as informações contidas no arquivo XML em um único DataFrame.

        :return: DataFrame
        '''
        Arquivo = self.Arquivo
        nota = parser.parse(self.Arquivo, silence=True)

        Arquivo.replace("nfe/", "")

        print(f"Processando NFe Nº (ID): {nota.infNFe.Id}")

        #INFORMAÇÕES DE IDENTIFICAÇÃO DA NF-E
        dict_ide = {"NFe_ID": None, "Arquivo": None}

        dict_ide['NFe_ID'] = nota.infNFe.Id

        dict_ide['Arquivo'] = Arquivo

        df_ide = pd.DataFrame(dict_ide, index=[0])

        #IDENTIFICAÇÃO DO EMITENTE DA NOTA FISCAL ELETRÔNICA
        dict_emit = {"CNPJ": None, "xNome": None, "xFant": None, "cMun": None, "xMun": None, "UF": None,
                     "CEP": None, "cPais": None, "xPais": None, "Arquivo": None}

        dict_emit['CNPJ'] = str(nota.infNFe.emit.CNPJ)
        dict_emit['xNome'] = nota.infNFe.emit.xNome
        dict_emit['xFant'] = nota.infNFe.emit.xFant
        dict_emit['cMun'] = nota.infNFe.emit.enderEmit.cMun
        dict_emit['xMun'] = nota.infNFe.emit.enderEmit.xMun
        dict_emit['UF'] = nota.infNFe.emit.enderEmit.UF
        dict_emit['CEP'] = nota.infNFe.emit.enderEmit.CEP
        dict_emit['cPais'] = nota.infNFe.emit.enderEmit.cPais
        dict_emit['xPais'] = nota.infNFe.emit.enderEmit.xPais

        dict_emit['Arquivo'] = Arquivo

        df_emit = pd.DataFrame(dict_emit, index=[0])

        #IDENTIFICAÇÃO DO DESTINATÁRIO DA NOTA FISCAL ELETRÔNICA
        dict_dest = {"CNPJ": None, "xNome": None, "cMun": None, "xMun": None, "UF": None, "CEP": None,
                     "cPais": None, "xPais": None, "Arquivo": None}

        dict_dest['CNPJ'] = str(nota.infNFe.dest.CNPJ)
        dict_dest['xNome'] = nota.infNFe.dest.xNome

        dict_dest['cMun'] = nota.infNFe.dest.enderDest.cMun
        dict_dest['xMun'] = nota.infNFe.dest.enderDest.xMun
        dict_dest['UF'] = nota.infNFe.dest.enderDest.UF
        dict_dest['CEP'] = nota.infNFe.dest.enderDest.CEP
        dict_dest['cPais'] = nota.infNFe.dest.enderDest.cPais
        dict_dest['xPais'] = nota.infNFe.dest.enderDest.xPais

        dict_dest['Arquivo'] = Arquivo

        df_dest = pd.DataFrame(dict_dest, index=[0])

        #INFORMAÇÕES DE IDENTIFICAÇÃO DA NF-E POR PRODUTO OU SERVIÇO
        dict_infNFe = { "chNFe": None, 'Arquivo': None}
        dict_infNFe['chNFe'] = str(nota.infNFe.Id).replace("NFe", "")

        dict_infNFe['Arquivo'] = Arquivo

        df_infNFe = pd.DataFrame(dict_infNFe, index=[0])

        #DETALHAMENTO DE PRODUTOS E SERVIÇOS DA NF-E
        list_dict_det = []
        # Loop para os n podutos da nota
        for i in nota.infNFe.det:
            dict_det = {"nItem": None, "cProd": None, "cEAN": None, "xProd": None, "NCM": None, "uCom": None,
                        "qCom": None, "vUnCom": None, "vProd": None, "uTrib": None, "qTrib": None, "vUnTrib": None,
                        "indTot": None, "vTotTrib": None, "det_icms_identity": None, "det_icms_orig": None,
                        "det_icms_CST": None, "det_icms_vBCSTRet": None, "det_icms_pST": None, "det_icms_modBC": None,
                        "det_icms_vBC": None, "det_icms_pICMS": None, "det_icms_vICMS": None, "det_icms_modBCST": None,
                        "det_icms_pMVAST": None, "det_icms_vBCST": None, "det_icms_pICMSST": None, "det_icms_vICMSST": None,
                        "det_icms_vICMSSubstituto": None, "det_icms_vICMSSTRet": None, "cEnq": None, "IPINT": None,
                        "PISNT": None, "COFINSNT": None, "PISAliq_CST": None, "PISAliq_vBC": None, "PISAliq_pPIS": None,
                        "PISAliq_vPIS": None, "COFINSAliq": None, "COFINSAliq_CST": None, "COFINSAliq_vBC": None,
                        "COFINSAliq_pCOFINS": None, "COFINSAliq_vCOFINS": None, "infAdProd": None, "IBS": None, "CBS": None,
                        "IVA": None, "TaxTotalRT": None, "ValorTotalRT": None, "Arquivo": None}

            try:
                dict_det['nItem'] = i.nItem
            except:
                None

            dict_det['Arquivo'] = Arquivo
            dict_det['cProd'] = i.prod.cProd
            dict_det['cEAN'] = i.prod.cEAN
            dict_det['xProd'] = i.prod.xProd
            dict_det['NCM'] = i.prod.NCM

            dict_det['uCom'] = i.prod.uCom
            dict_det['qCom'] = i.prod.qCom
            dict_det['vUnCom'] = i.prod.vUnCom
            dict_det['vProd'] = i.prod.vProd

            dict_det['uTrib'] = i.prod.uTrib
            dict_det['qTrib'] = i.prod.qTrib
            dict_det['vUnTrib'] = i.prod.vUnTrib
            dict_det['indTot'] = i.prod.indTot

            #TRIBUTOS INCIDENTES NO PRODUTO OU SERVIÇO
            dict_det['vTotTrib'] = i.imposto.vTotTrib

            # ICMS
            impostos = {
                "ICMS10": i.imposto.ICMS.ICMS10
                , "ICMS20": i.imposto.ICMS.ICMS20
                , "ICMS30": i.imposto.ICMS.ICMS30
                , "ICMS40": i.imposto.ICMS.ICMS40
                , "ICMS51": i.imposto.ICMS.ICMS51
                , "ICMS60": i.imposto.ICMS.ICMS60
                , "ICMS70": i.imposto.ICMS.ICMS70
                , "ICMS90": i.imposto.ICMS.ICMS90
                , "ICMSPart": i.imposto.ICMS.ICMSPart
                , "ICMSST": i.imposto.ICMS.ICMSST
                , "ICMSSN101": i.imposto.ICMS.ICMSSN101
            }

            for imposto in impostos:
                try:
                    dict_det['det_icms_identity'] = imposto
                    dict_det['det_icms_orig'] = impostos[imposto].orig
                    dict_det['det_icms_CST'] = impostos[imposto].CST
                    # + *
                    dict_det['det_icms_vBCSTRet'] = impostos[imposto].vBCSTRet
                    # + *
                    dict_det['det_icms_pST'] = impostos[imposto].pST
                    # -
                    dict_det['det_icms_modBC'] = impostos[imposto].modBC
                    # -
                    dict_det['det_icms_vBC'] = impostos[imposto].vBC
                    # -
                    dict_det['det_icms_pICMS'] = impostos[imposto].pICMS
                    dict_det['det_icms_vICMS'] = impostos[imposto].vICMS
                    # -
                    dict_det['det_icms_modBCST'] = impostos[imposto].modBCST
                    # -
                    dict_det['det_icms_pMVAST'] = impostos[imposto].pMVAST
                    # -
                    dict_det['det_icms_vBCST'] = impostos[imposto].vBCST
                    # -
                    dict_det['det_icms_pICMSST'] = impostos[imposto].pICMSST
                    # -
                    dict_det['det_icms_vICMSST'] = impostos[imposto].vICMSST
                    dict_det['det_icms_vICMSSubstituto'] = impostos[imposto].vICMSSubstituto
                    # + *
                    dict_det['det_icms_vICMSSTRet'] = impostos[imposto].vICMSSTRet
                    break
                except:
                    None
            # ICMS/

            # IPI
            dict_det['cEnq'] = i.imposto.IPI.cEnq
            try:
                dict_det['IPINT'] = i.imposto.IPI.IPINT.CST
            except:
                None
            # IPI/

            # PIS
            try:
                dict_det['PISNT'] = i.imposto.PIS.PISNT.CST
            except:
                None
            # PIS/

            # COFINS
            try:
                dict_det['COFINSNT'] = i.imposto.COFINS.COFINSNT.CST
            except:
                None
            # COFINS/

            # Aliq
            try:
                dict_det['PISAliq_CST'] = i.imposto.PIS.PISAliq.CST
            except:
                None
            try:
                dict_det['PISAliq_vBC'] = i.imposto.COFINS.PISAliq.vBC
            except:
                None
            try:
                dict_det['PISAliq_pPIS'] = i.imposto.PIS.PISAliq.pPIS
            except:
                None
            try:
                dict_det['PISAliq_vPIS'] = i.imposto.COFINS.PISAliq.vPIS
            except:
                None

            try:
                dict_det['COFINSAliq'] = i.imposto.PIS.COFINSAliq
            except:
                None

            try:
                dict_det['COFINSAliq_CST'] = i.imposto.PIS.COFINSAliq.CST
            except:
                None
            try:
                dict_det['COFINSAliq_vBC'] = i.imposto.COFINS.COFINSAliq.vBC
            except:
                None
            try:
                dict_det['COFINSAliq_pCOFINS'] = i.imposto.PIS.COFINSAliq.pCOFINS
            except:
                None
            try:
                dict_det['COFINSAliq_vCOFINS'] = i.imposto.COFINS.COFINSAliq.vCOFINS
            except:
                None

            # infAdProd
            try:
                dict_det['infAdProd'] = i.infAdProd
            except:
                None

            # infAdProd/
            Vprod = float(i.prod.vProd)
            nNCM = int(i.prod.NCM)

            tax = TaxCalculator(nNCM, Vprod)

            dict_det['IBS'] = tax.IBScalc()
            dict_det['CBS'] = tax.CBScalc()
            dict_det['IVA'] = tax.IVAcalc()
            dict_det['TaxTotalRT'] = Vprod - (tax.IVAcalc())
            dict_det['ValorTotalRT'] = tax.IVAcalc()
            dict_det['Arquivo'] = Arquivo

            list_dict_det.append(dict_det)

        if len(list_dict_det) > 0:
            df_det = pd.DataFrame(list_dict_det)
        else:
            df_det = pd.DataFrame(list_dict_det, index=[0])

        #VALORES TOTAIS DA NF-E
        dict_total = {"vBC": None, "vICMS": None, "vICMSDeson": None, "vFCPUFDest": None,
                      "vICMSUFDest": None, "vICMSUFRemet": None, "vFCP": None, "vBCST": None, "vST": None,
                      "vFCPST": None, "vFCPSTRet": None, "vProd": None, "vFrete": None, "vSeg": None, "vDesc": None,
                      "vII": None, "vIPI": None, "vIPIDevol": None, "vPIS": None, "vCOFINS": None, "vOutro": None,
                      "vNF": None, "vTotTrib": None, "Arquivo": None
                      }

        # total
        # ICMSTot
        dict_total['vBC'] = nota.infNFe.total.ICMSTot.vBC
        dict_total['vICMS'] = nota.infNFe.total.ICMSTot.vICMS
        dict_total['vICMSDeson'] = nota.infNFe.total.ICMSTot.vICMSDeson
        dict_total['vFCPUFDest'] = nota.infNFe.total.ICMSTot.vFCPUFDest
        dict_total['vICMSUFDest'] = nota.infNFe.total.ICMSTot.vICMSUFDest
        dict_total['vICMSUFRemet'] = nota.infNFe.total.ICMSTot.vICMSUFRemet
        dict_total['vFCP'] = nota.infNFe.total.ICMSTot.vFCP
        dict_total['vBCST'] = nota.infNFe.total.ICMSTot.vBCST
        dict_total['vST'] = nota.infNFe.total.ICMSTot.vST
        dict_total['vFCPST'] = nota.infNFe.total.ICMSTot.vFCPST
        dict_total['vFCPSTRet'] = nota.infNFe.total.ICMSTot.vFCPSTRet
        dict_total['vProd'] = nota.infNFe.total.ICMSTot.vProd
        dict_total['vFrete'] = nota.infNFe.total.ICMSTot.vFrete
        dict_total['vSeg'] = nota.infNFe.total.ICMSTot.vSeg
        dict_total['vDesc'] = nota.infNFe.total.ICMSTot.vDesc
        dict_total['vII'] = nota.infNFe.total.ICMSTot.vII
        dict_total['vIPI'] = nota.infNFe.total.ICMSTot.vIPI
        dict_total['vIPIDevol'] = nota.infNFe.total.ICMSTot.vIPIDevol
        dict_total['vPIS'] = nota.infNFe.total.ICMSTot.vPIS
        dict_total['vCOFINS'] = nota.infNFe.total.ICMSTot.vCOFINS
        dict_total['vOutro'] = nota.infNFe.total.ICMSTot.vOutro
        dict_total['vNF'] = nota.infNFe.total.ICMSTot.vNF
        dict_total['vTotTrib'] = nota.infNFe.total.ICMSTot.vTotTrib
        dict_total['Arquivo'] = Arquivo
        # ICMSTot
        # total

        df_total = pd.DataFrame(dict_total, index=[0])

        #DICT PARA DATAFRAME
        df_ = df_ide.merge(df_emit, how="left", on="Arquivo")
        df_ = df_.merge(df_dest, how="left", on="Arquivo")
        df_ = df_.merge(df_infNFe, how="left", on="Arquivo")
        df_ = df_.merge(df_det, how="left", on="Arquivo")
        df_ = df_.merge(df_total, how="left", on="Arquivo")

        return df_


class CSVWriter:
    def __init__(self):
        '''
        Retorna um arquivo CSV a partir de um DataFrame que contenha informações de uma NFe, uma vez que a identificação da nota é necessária.

        :param self:
        :return: None
        '''
        self.dataframe = None

    def saveONEnfe(self, df, Arquivo):
        '''
        Retorna um arquivo CSV, nomeado com a ID da NFe, na pasta 'output'.

        :param self:
        :param df: DataFrame
        :param Arquivo: str
        :return: CSV
        '''
        self.df = df
        self.Arquivo = Arquivo

        xml_id = NFExtractor(self.Arquivo)

        nfe_id = xml_id.NfeID()

        # Salvar CSV
        self.df.to_csv(f"OUTPUT/{nfe_id}.csv", sep=";", encoding="utf8", index=False)


    def saveALLnfe(self, collection):
        '''
        Retorna um arquivo CSV composto por um ou mais DataFrames contidos em lista.

        :param self:
        :param collection: list
        :return: CSV
        '''
        self.collection = collection

        # Unir todas as NFe
        df_merged = pd.concat(self.collection)

        # Salvar CSVs
        df_merged.to_csv("OUTPUT/Collection.csv", sep=";", encoding="utf8", index=False)
