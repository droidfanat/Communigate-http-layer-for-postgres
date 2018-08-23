from TfopLib import TfopSe, Tfop


tfopse = TfopSe()

tfopse.add(Tfop("222","operator_name","10.10.10.2","operator.domain.com","441"))
tfopse.add(Tfop("333","operator_name","10.10.10.3","operator.domain1.com","442"))
tfopse.add(Tfop("444","operator_name","10.10.10.4","operator.domain2.com","443"))
tfopse.add(Tfop("555","operator_name","10.10.10.5","operator.domain3.com","*"))

tfopse.file_save('./tfop.json')
