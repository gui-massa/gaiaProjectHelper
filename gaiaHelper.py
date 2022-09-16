lista_planetas = ["blue", "red", "orange", "yellow", "brown", "grey", "white"]
lista_povos = ["Terranos","Lantids", "Hadsh Hallas", "Ivits", "Geodens", "Bal T'arks", "Xenos", "Gleens", "Taklons", "Ambas", "Firaks", "Mad Droids", "Nevlas", "Itars"]
track_names = ["Terraformação", "Navegação", "Inteligência Artificial", "Gaiaformação", "Economia", "Ciência"]

class Player:
    
    def __init__(self, name: str, board: int):
        """
        Args:
            name (str): Nome do jogador.
            board (int): Board esclhido na ordem do manual. De 1 a 14.
        """
        self._name = name
        self._board = board
        self._track = [0, 0, 0, 0, 0, 0]
        self._gaiaformers = 0
        self._custo_gaia = 1000
        self._energy_charge = [0]
        self._energy_token_generation = []
        self._structures = [0, 0, 0, 0, 0] #order = mina, comercio, laboratório, academia, instituto 
        
        if self._board == 1:
            print("Terranos")
            self._home_planet = "blue"
            self._energy = [0, 2, 4, 0]
            self._resources = [4, 15, 3, 1] #order = minerio, gold, science, ciq
            self._resource_generation = [1, 0, 1, 0]
            self.avanca_track(3, free=True)
            
        # creating the terraforming cost for each planet:
        #order = blue, red, orange, yellow, brown, grey, white
        if self._home_planet == "blue": planet_index = 7
        elif self._home_planet == "red": planet_index = 6
        elif self._home_planet == "orange": planet_index = 5
        elif self._home_planet == "yellow": planet_index = 4
        elif self._home_planet == "brown": planet_index = 3
        elif self._home_planet == "grey": planet_index = 2
        elif self._home_planet == "white": planet_index = 1
        terraplan_base = [0, 1, 2, 3, 3, 2, 1, 0, 1, 2, 3, 3, 2, 1, 0]
        self._terraplan = []
        for idx, planet in enumerate(range(7)):
            self._terraplan.append(terraplan_base[idx+planet_index])
        self._terraplan.append(0)
        self._terraplan.append(0)
        print("Terraforming cost = ", self._terraplan)


    def __str__(self) -> str:	
        return self._name + " -> " + lista_povos[self._board - 1]
    
    
    def gain_resource(self, minerio, cash, science, ciq):
        """
        Args:
            minerio (int): Minerio a ser gerado para o jogador instantaneamente
            cash (int): Dinheiro a ser gerado para o jogador instantaneamente
            science (int): Ciência a ser gerado para o jogador instantaneamente
            ciq (int): C.I.Q a ser gerado para o jogador instantaneamente
        """
        self._resources[0] += minerio
        self._resources[1] += cash
        self._resources[2] += science
        self._resources[3] += ciq
    
    
    def raise_generation(self, minerio:int, cash:int, science:int, ciq:int):
        """
        Args:
            minerio (int): Minerio a ser acrescido na geração no início de cada turno.
            cash (int): Dinheiro a ser acrescido na geração no início de cada turno.
            science (int): Ciência a ser acrescido na geração no início de cada turno.
            ciq (int): C.I.Q a ser acrescido na geração no início de cada turno.
        """
        self._resource_generation[0] += minerio
        self._resource_generation[1] += cash
        self._resource_generation[2] += science
        self._resource_generation[3] += ciq
    
    
    def pay(self, minerio: int, cash: int, science: int, ciq: int): #usando zip para fins de estudo
        """
        Args:
            minerio (int): Minério a ser pago para a ação ser completa.
            cash (int): Dinheiro a ser pago para a ação ser completa.
            science (int): Ciência a ser pago para a ação ser completa.
            ciq (int): C.I.Q a ser pago para a ação ser completa.

        Returns:
            _type_: _description_
        """
        if  (minerio <= self._resources[0] and
                cash <= self._resources[1] and
                science <= self._resources[1] and
                ciq <= self._resources[1]):
            cost = [-minerio, -cash, -science, -ciq]
            zipped_resources = zip(self._resources, cost)
            self._resources = [sum(resource) for resource in zipped_resources]
            return True
        else: 
            print("Sem recursos suficientes.")
            return False
    
    
    def make_mine(self, planet: int, ciqs_used: int):
        """
        Args:
            planet (int): Número do planeta:
                blue -> 0 |
                red -> 1 |
                orange -> 2 |
                yellow -> 3 |
                brown -> 4 |
                grey -> 5 |
                white -> 6 |
                GaiaGreen -> 7 | 
                Gaiaformed -> 8 |
            ciqs_used (int): Considerar aqui o número total de C.I.Q usado, para distância e gaiaformação(se necessário).
        """
        print("\n Fazendo mina:")
        # Checking terraforming track
        if self._track[0] < 2:
            self._terracost = 3
        elif self._track[0] < 3:
            self._terracost = 2
        else:
            self._terracost = 1
        
        if self._structures[0] < 8:
            payed = self.pay((1 + self._terraplan[planet] * self._terracost), 2, 0, ciqs_used)
            if payed == True:
                self._structures[0] += 1
            if planet == 8:
                self._gaiaform += 1
        else: print("Número máximo de minas atingido")

    
    def upgrade_mine_to_comercio(self, close_to_neighbour:bool=False):
        """_summary_

        Args:
            close_to_neighbour (bool): True caso haja uma estrutura inimiga a até 2 espaços de distância. Default to False.
        """
        print("\n Upgrade para comercio:")
        if close_to_neighbour == True:
            cost_cash = 3
        else:
            cost_cash = 6
        
        if self._structures[0] >= 1 and self._structures[1] < 8:
            payed = self.pay(2, cost_cash, 0, 0)
            if payed == True:
                self._structures[0] -= 1
                self._structures[1] += 1
        else: print("Não há minas disponíveis para upgrade, ou atingido o número máximo de comércios.")


    def upgrade_comercio_to_lab(self):
        print("\n Upgrade para laboratório de pesquisa:")
        if self._structures[1] >= 1 and self._structures[2] < 3:
            payed = self.pay(3, 5, 0, 0)
            if payed == True:
                self._structures[1] -= 1
                self._structures[2] += 1
                print("Escolha uma tecnologia e avance no respectivo track!")
        else: print("Não há estações de comércio disponíveis para upgrade, ou atingido o máximo de laboratórios.")
        
        
    def upgrade_comercio_to_instituto(self):
        print("\n Upgrade para instituto planetário:")
        if self._structures[1] >= 1 and self._structures[4] < 1:
            payed = self.pay(4, 6, 0, 0)
            if payed == True:
                self._structures[1] -= 1
                self._structures[4] += 1
                print("Veja o bônus desbloqueado!")
        else: print("Não há estações de comércio disponíveis para upgrade, ou você já possui o instituto.")
                
        
    def upgrade_lab_to_academia(self):
        print("\n Upgrade para academia:")
        if self._structures[2] >= 1 and self._structures[3] < 2:
            payed = self.pay(4, 6, 0, 0)
            if payed == True:
                self._structures[1] -= 1
                self._structures[4] += 1
                print("Veja o bônus desbloqueado!")
        else: print("Não há estações de comércio disponíveis para upgrade.")
        
        
    def avanca_track(self, track_number:int, free=False):
        """
        Args:
            track_number (int): Terraformação -> 0, Navegação -> 1, Inteligência Artificial -> 2, Projeto Gaia -> 3, Economia -> 4, Ciência -> 5]
            free (bool, optional): True se for uma ação de avanço no sem necessidade de pagar ciência, como pegar uma tecnologia ou avanços específicos de algum board. Defaults to False.
        """
        payed = False
        if free == False:
            payed = self.pay(0,0,4,0)
        if payed == True or free == True:
            self._track[track_number] += 1 
            print(f"Tecnologia {track_names[track_number]} avançou para a casa {self._track[track_number]}.")

            # Terraforming track bonuses:
            if track_number == 0:
                if self._track[0] in [1,4]:
                    print("Ganhou 2 minérios!")
                    self._resources[0] += 2
                elif self._track[0] == 5:
                    print("Ganhou uma aliança! Nãp esqueça de computar recursos e pontos.")
            
            # Navigation track bonuses:
            elif track_number == 1:
                if self._track[1] in [1,3]:
                    print("Ganhou 1 c.i.q!")
                    self._resources[0] += 2
                elif self._track[1] == 5:
                    print("Ganhou um planeta misterioso para colocar em qualquer lugar do mapa!")
                    print("Este conta também como uma mina para qualquer propósito.")


            # A.I track bonuses:
            elif track_number == 2: 
                if self._track[2] in [1,2]:
                    print("Ganhou 1 c.i.q!")
                    self._resources[3] += 1
                elif self._track[2] in [3,4]:
                    print("Ganhou 2 c.i.q!")
                    self._resources[3] += 2
                elif self._track[2] in [5]:
                    print("Ganhou 4 c.i.q!")
                    self._resources[3] += 4

            # Gaiaforming track bonuses:
            elif track_number == 3: 
                if self._track[3] in [1,3,4]:
                    print("Ganhou um Gaiaformador!")
                    self._gaiaformers += 1
                    if self._track[3] == 1:
                        self._custo_gaia = 6
                    elif self._track[3] == 3:
                        self._custo_gaia = 4
                    elif self._track[3] == 4:
                        self._custo_gaia = 3
                elif self._track[3] == 2:
                    for i in range(3):
                        self.gain_power_token()
                elif self._track[3] == 5:
                    print("Compute seus pontos!")
            
            # Resource Track bonuses:
            elif track_number == 4: 
                if self._track[4] == 1:
                    self._resource_generation[1] += 2
                    self._energy_charge[0] += 1
                elif self._track[4] == 2:
                    self._resource_generation[0] += 1
                    self._energy_charge[0] += 1
                elif self._track[4] == 3:
                    self._resource_generation[1] += 1
                    self._energy_charge[0] += 1
                elif self._track[4] == 4:
                    self._resource_generation[0] += 1
                    self._resource_generation[1] += 1
                    self._energy_charge[0] += 1
                elif self._track[4] == 5:
                    self._resources[0] += 3
                    self._resources[1] += 6
                    for i in range(6):
                        self.charge_1_power()

            # Science Track bonuses:
            elif track_number == 5: 
                if self._track[5] in [1, 2, 3, 4]:
                    self._resource_generation[2] += 1
                elif self._track[5] == 5:
                    self._resources[2] += 9


    def charge_1_power(self):
        if self._energy[1] > 0:
            self._energy[1] -= 1
            self._energy[2] += 1

        elif self._energy[1] == 0 and self._energy[2] != 0:
            self._energy[2] -= 1
            self._energy[3] += 1

        else:
            print("Energia já está no máximo! Energia não carregada.")
            
            
    def force_charge(self):
        if self._energy[2] >= 2:
            self._energy[2] -= 2
            self._energy[3] += 1
            if self._board == 14: #Itars
                self._energy[0] += 1
        else:
            print("Sem energia suficiente na energy pool 2.")
    
    
    def gain_power_token(self):
        self._energy[1] += 1
        
        
    def new_power_generator(self, energy_generated):
        self._energy_charge.append(energy_generated)
        
    
    def gaiaform(self):
        print("Gaiaformando planeta Transdimensional")
        if self._gaiaformers > 0: 
            if sum(self._energy) >= self._custo_gaia:
                for energy in range(self._custo_gaia):
                    if self._energy[1] > 0:
                        self._energy[1] -= 1
                        self._energy[0] += 1
                    elif self._energy[2] > 0:
                        self._energy[2] -= 1
                        self._energy[0] += 1
                    else:
                        self._energy[3] -= 1
                        self._energy[0] += 1
            else: print("Sem tokens de energia suficientes para gaiaformar")
        else: print("Você não tem Gaiaformadores disponíveis")
    
    
    def fase_renda(self, minerio=0, cash=0, science=0, ciq=0, new_power_tokens=False, energy_charge=False):
        """
        Os parâmetros a serem passados são os da ficha de turno escolhida ao passar o turno passado.
        """
        print("Fase de renda:")
        print(f"Recursos Antes {self._resources}")
        self.gain_resource(minerio, cash , science, ciq)
        self.gain_resource(self._resource_generation[0], self._resource_generation[1], self._resource_generation[2], self._resource_generation[3],)
        print(f"Recursos a gerar {self._resource_generation}")
        if energy_charge != False:
            self._energy_charge.append(energy_charge)
        if new_power_tokens != False:
            self._energy_token_generation.append(new_power_tokens)
        print(f"Recursos depois {self._resources}")
        
        # Analisar como resolver as gerações de energia, pois a ordem pode influenciar. Talvez com um "if" garantindo que a energia pode ser carregada por inteiro antes de carregar a energia, e se não puder, aí sim considerar ativar um token. Considerar também tentar primeira a geração maior, depois a menor. EDIT: É sempre opção do jogador, às vezes é preferível que a energia seja carregada de forma menos eficiente, dependendo do povo utilizado. Implementar desta forma futuramente.
        # Criação do board de geração de energia visual (energy pool)
        print()
        print(f"Status da energia: {self._energy}")
        print("Energy pool GAIA:", end="")
        for energy in range(self._energy[0]):
            print(" 0", end="")
        print()
        print("Energy pool I   :", end="")
        for energy in range(self._energy[1]):
            print(" 0", end="")
        print()
        print("Energy pool II  :", end="")
        for energy in range(self._energy[2]):
            print(" 0", end="")
        print()
        print("Energy pool III :", end="")
        for energy in range(self._energy[3]):
            print(" 0", end="")            
        print()
        print(f"Ações de novo token de energia: {self._energy_token_generation}") 
        print(f"Ações de geração de energia: {self._energy_charge}")

        #removendo gerações não desejadas para o pŕoximo turno, que podem ter sido adicionadas na função fase_renda()
        if new_power_tokens != False:
            self._energy_token_generation.pop()

        if energy_charge != False:
            self._energy_charge.pop()
            
        
    def fase_gaia(self):
        print("Fase Gaia iniciada.")
        for energy in range(self._energy[0]):
            self._energy[0] -= 1
            self._energy[1] += 1
    
            
    def general_status(self):
        print()
        print(self)
        print()
        print(f"Minério = {self._resources[0]}")
        print(f"Dinheiro = {self._resources[1]}")
        print(f"Ciência = {self._resources[2]}")
        print(f"C.I.Q = {self._resources[3]}")
        print()
        print(f"Minas = {self._structures[0]}")
        print(f"Comércios = {self._structures[1]}")
        print(f"Laboratórios = {self._structures[2]}")
        print(f"Academias = {self._structures[3]}")
        print(f"Instituto Planetário = {self._structures[4]}")
        print()
        print(f"Energy Pool = {self._energy}")
        print()
    
    
    