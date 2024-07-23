

class Solution(object):
    def addBinary(self, a, b):
        r = []
        res = int(a, 2) + int(b, 2)
        if res == 0:
            return '0'
        while res > 0:
            d = res % 2
            r.append(str(d))
            res = res //2
        return str(''.join(r[::-1]))
    

    
    # def inventory_read(self):
    #     pass


    # def inventory_update(self):
    #     pass


    # def inventory_delete(self):
    #     pass