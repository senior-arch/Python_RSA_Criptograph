class SimpleHash:
    @staticmethod
    def hash_message(message):
        hash_value = 0xABCDEF  # Um valor inicial fixo
        prime = 31  # Usamos um número primo pequeno

        for char in message:
            # Atualiza o hash_value usando operações bit a bit
            hash_value = (hash_value * prime) ^ ord(char)
            hash_value = hash_value & 0xFFFFFFFFFFFFFFFF  # Limita a 64 bits

        # Converte o hash_value final para hexadecimal
        return hex(hash_value)
