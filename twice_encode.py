class Twice_encode:

    #['S1', 'F4', 'F7', 'N1', 'F2', 'N24', 'N3', 'N4', 'F8', 'N2', 'F10', 'N11', 'N5', 'N6', 'F5', 'N7', 'F1', 'F11', 'F
    # 3', 'S2']
    #['A', 'B', 'C', 'D', 'E',  'G', 'H', 'I', 'J', 'K', 'L', 'M',  'O', 'P', 'Q', 'R',  'T', 'U', 'V', 'W']
    dict_code={'F1': 'T', 'N11': 'M', 'N6': 'P', 'N4': 'I', 'S2': 'W', 'F11': 'U', 'S1': 'A', 'N2': 'K', 'F7': 'C', \
               'N1': 'D', 'N7': 'R', 'F2': 'E', 'F3': 'V', 'N5': 'O', 'F10': 'L', 'F4': 'B', 'F8': 'J', 'N24': 'G', 'N3'
               : 'H', 'F5': 'Q'}

    def Sea2Tcode(self,s):
        from RunLenCode import RLC
        r = RLC()
        str=r.Sea2Code(s)
        for key,value in self.dict_code.items():
            str=str.replace(key,value)

        return str

    def Tcode2Sea(self,str):
        from RunLenCode import RLC
        r = RLC()
        for key,value in self.dict_code.items():
            str=str.replace(value,key)

        s=r.Code2Sea(str)
        return s