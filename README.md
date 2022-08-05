# Random TDMA

This repository implements the suggested algorithm-3 of the papper [1], which refers to a Random TDMA algorithm. In the context of this algorithm a passive star (coupler) system simulator was developed, so that it could be easy to modify the routing algorithm and simulate any of available algorithms that can apply at architecture of a Passive Star.

### Sequence Diagram of Code Execution

```mermaid
sequenceDiagram
	Node-i->>Coupler:HelloMessage
	note right of Coupler: Add new Node at Coupler's Map
	Coupler->>Node-i:WelcomeMessage
	Coupler-->Node-i: Procedure starting
	loop Random TDMA
			note left of Node-i: With possibility-P
			loop Message Generation
				Node-i-->Node-i: Select a Random-Channel (R-Channel)
				Node-i-->Node-i: Select a Random-Node which listen at R-Channel
				Node-i->>Node-i: Create new Message
			end
			Coupler->>Coupler: Create new Packet
			Coupler-->Coupler: Random selects Node for each Channel
			loop Receive Message
        Coupler->>Node-i: You have been selected, to transmit at C-channnel
        note left of Node-i: If I have Message for C-channel
        Node-i->>Node-i: Pop-Message from C-Buffer Update Stats
        Node-i-->Node-i: Update Stats
        Node-i->>Coupler: Message
      end
      note right of Coupler: Receive Message for selected nodes
      Coupler->>Coupler: Send Packet
      Node-i->>Node-i: Receive Message from R-Channel
      note left of Node-i: If there is a Message for me at R-Channel
	end
```



### Results

![RandomTDMA_Diagramm](https://github.com/szZzr/random-tdma/blob/master/RandomTDMA_Diagramm.png)

#### Bibliography

[1] Ganz, A. and Koren, Z., 1991, January. WDM passive star-protocols and performance analysis. In *IEEE INFCOM'91-Communications Societies Proceedings* (pp. 991-992). IEEE Computer Society.
