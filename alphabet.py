class Alphabet():
    @staticmethod
    def get_alphabet_dict(language):
        if language == 'georgian':
            alphabet_dict = {
                'a': 'ა',
                'b': 'ბ',
                'g': 'გ',
                'd': 'დ',
                'e': 'ე',
                'v': 'ვ',
                'w': 'ვ',
                'z': 'ზ',
                't': 'თ',
                'i': 'ი',
                "k'": 'კ',
                'l': 'ლ',
                'm': 'მ',
                'n': 'ნ',
                'o': 'ო',
                'p': 'პ',
                'zh': 'ჟ',
                'r': 'რ',
                's': 'ს',
                "t'": 'ტ',
                'u': 'უ',
                'p,f': 'ფ',
                'k': 'ქ',
                'gh': 'ღ',
                'q': 'ყ',
                'sh': 'შ',
                'ch': 'ჩ',
                'ts': 'ც',
                'c': 'ც',
                'dz': 'ძ',
                "ts'": 'წ',
                "ch'": 'ჭ',
                'kh': 'ხ',
                'x': 'ხ',
                'j': 'ჯ',
                'h': 'ჰ'
            }
            return alphabet_dict
        else:
            return f'Язык {language} не поддерживается'
