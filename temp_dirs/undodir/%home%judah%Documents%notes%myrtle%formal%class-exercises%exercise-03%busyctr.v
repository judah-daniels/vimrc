Vim�UnDo� mM���аU���c�<iA��>��unU	���   o                                   b��:    _�                    M        ����                                                                                                                                                                                                                                                                                                                            M           V                   b��'    �   U   W           �   T   V                      o_busy <= 1;�   S   U                  else �   R   T          &            o_busy <= i_start_signal ;�   Q   S                  else if (counter == 0)�   P   R                      o_busy <= 0;�   O   Q          $        if (i_reset || counter == 1)�   N   P           �   M   O              always @(posedge i_clk)�   L   N              initial o_busy = 0;5�_�                    I       ����                                                                                                                                                                                                                                                                                                                            M           V                   b��5     �   H   J          	/* always @(*) */5�_�                     J       ����                                                                                                                                                                                                                                                                                                                            M           V                   b��9    �   I   K          !	/* 	o_busy <= (counter != 0); */5�_�                    M       ����                                                                                                                                                                                                                                                                                                                                                             b��     �   L   O   o      /    initial o_busy = 0; always @(posedge i_clk)5�_�                     M       ����                                                                                                                                                                                                                                                                                                                                                             b��     �   L   O   n      0    initial o_busy = 0; always @(posedge i_clk) 5��