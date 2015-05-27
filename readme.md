Uruchomienie
============

0. Trainer:
    * cd algorithms/letter_recognition_simple && python trainer_svd.py

1. Webservice:
    * cd webservice && mpiexec -np 11 python2.7 runner.py "plik_konfiguracyjny" "port"
    * uruchamia się usługa na porcie 10240
    
2. Front:
    * python2.7 gui/gui.py "port"
    * uruchamia się na porcie "port"
    * -> IP:10241 i można rysować