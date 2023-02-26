# Demo_C
Tato sada souborů demonstruje různé způsoby implementace klient-server pomocí BSD soketů.
Implementace slouží pouze pro demonstraci principů a ve většině případů jim chybí správné a dostatečné ošetření 
všech možných chyb, které mohou nastat.

*Vyzkoušeno v Ubuntu 16.04.3 LTS.*

## DemoBlock
Implementace TCP serveru, který používá blokující sokety. Tento server představuje 
základní postup vytvoření serveru pomocí knihovny soketů. Server pouze vypisuje
zprávy, které klient posílá. 
Použití:

```
./server 11111 
```

``` 
telnet localhost 11111
```

## DemoFork
Server, který používá funkce `fork` pro vytvoření procesu obsluhy požadavků. Tímto je umožněno zpracování více požadavků od klientů zároveň. 

```
./server 11111 
```

``` 
telnet localhost 11111
```

## DemoMessenger
Implementuje triviální SMTP klient, který umožňuje posílat e-mail zprávy. 
Tento nástroj demonstruje základy SMTP komunikace.

```
./messenger -s kazi.fit.vutbr.cz
```

## DemoNonBlock
Demonstrace serveru, který používá neblokující režim soketů a aktivně čeká na požadavky klienta. Tato implementace ukazuje problém aktivního čekání - zbytečná zátěž CPU. Pro demonstraci server vypisuje znak `.` pokaždé, když 
je vráceno `E_WOULDBLOCK` z volání operace neblokujícího soketu.
Použití:

```
./server 11111 
```

``` 
telnet localhost 11111
```

## DemoSelect
Ukazuje použití funkce `select` při využití neblokujících operací. Tento server vypisuje zprávy 
od klienta a také umožňuje zasílání zpráv od serveru. Toto je možné v libovolný okamžik, právě kvůli použití  `select`  a neblokujících operací. 
Použití:

```
./server 11111 
```

``` 
telnet localhost 11111
```

## DemoTcp
Demonstrace základních principů klient/server komunikace pomocí protokolu TCP. Implementuje obě strany komunikace. 
Klient se připojí k serveru a pošle zprávu. Server pouze odpoví stejnou zprávou a poté je komunikace ukončena. 
Použití:

```
./server 11111 
```

``` 
./client localhost 11111
```

## DemoUdp
Demonstrace základních principů klient/server komunikace pomocí protokolu UDP. Implementuje obě strany komunikace. 
Klient se připojí k serveru a pošle zprávu. Server pouze odpoví stejnou zprávou a poté je komunikace ukončena. 
Použití:

```
./server 11111 
```

``` 
./client localhost 11111
```

## SimpleIPv6
Ukázka serveru, který podporuje IPv6 protokol. Podobné jako DemoBlock, ale v IPv6.