#modbus单文件读取
import time
import struct

class modbus:
    def __init__(self,slaver,serial):
        self.data=[0x01,0x06,0x03,0xed,0x03,0x42,0xe4,0x7b]
        self.data[0]=slaver
        self.slaver=slaver
        self.uart = serial
        
    def ReadFloat(self,*args,reverse=False):
        for n,m in args:
            n,m = '%04x'%abs(n),'%04x'%abs(m)
        if reverse:
            v = n + m
        else:
            v = m + n
        y_bytes = []
        j=0
        for i in range(0,len(v),2):
            y_bytes.append(int(v[i:i+2],16))
        y_bytes=bytes(y_bytes)
        y = struct.unpack('!f',y_bytes)[0]
        y = round(y,6)
        return y

    def WriteFloat(self,value,reverse=False):
        value = struct.pack('!f',value)
        print(value)
        y_hex = ''.join(['%02x' % i for i in value])
        print(y_hex)
        n,m = y_hex[:-4],y_hex[-4:]
        n,m = int(n,16),int(m,16)
        if reverse:
            v = [n,m]
        else:
            v = [m,n]
        return v

    def calc_crc(self):
        crc = 0xFFFF
        for pos in self.data[:-2]:
            crc ^= pos
            for i in range(8):
                if ((crc & 1) != 0):
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        self.data[-2]=int(hex(crc & 0xff))
        self.data[-1]=int(hex(crc >> 8))

    def uart_write(self):
        self.calc_crc()
        self.uart.read()
        self.uart.write(bytearray(self.data))
        time.sleep_ms(25)
        return self.uart.read()
    
    def get_int(self,add):
        if(add>=1 and add<10000):
            self.data[1]=0x01
            self.data[2]=int(hex((add-1)>> 8))
            self.data[3]=int(hex((add-1)&0xff))
        if(add>=10000 and add<20000):
            self.data[1]=0x02
            self.data[2]=int(hex((add-10001)>> 8))
            self.data[3]=int(hex((add-10001)&0xff))
        if(add>=30000 and add<40000):
            self.data[1]=0x04
            self.data[2]=int(hex((add-30001)>> 8))
            self.data[3]=int(hex((add-30001)&0xff))
        if(add>=40000 and add<50000):
            self.data[1]=0x03
            self.data[2]=int(hex((add-40001)>> 8))
            self.data[3]=int(hex((add-40001)&0xff))
        if(add>=50000 or (add>=20000 and add<30000) or add<1):
            return '请检查，未发现(add>=50000 or (add>=20000 and add<30000) add<1)范围内的寄存器地址'
        self.data[4]=0x00
        self.data[5]=0x01
        read_data=self.uart_write()
        if(add>=1 and add<20000):
            return read_data[3]
        return read_data[3]*256+read_data[4]

    def set_int(self,add,data):
        if(add>=1 and add<10000):
            self.data[1]=0x05
            self.data[2]=int(hex((add-1)>> 8))
            self.data[3]=int(hex((add-1)&0xff))
            if (data==1):
                self.data[4]=0xFF
            else:
                self.data[4]=0x00
            self.data[5]=0x00
        if(add>=40000 and add<50000):
            self.data[1]=0x06
            self.data[2]=int(hex((add-40001)>> 8))
            self.data[3]=int(hex((add-40001)&0xff))
            self.data[4]=int(hex((data)>> 8))
            self.data[5]=int(hex((data)&0xff))
        read_data=self.uart_write()
        if(add>=1 and add<10000):
            return 0 if read_data[4]==0 else 1
        return read_data[4]*256+read_data[5]

    def get_float(self,add,reverse=False):
        return self.ReadFloat([self.get_int(add),self.get_int(add+1)],reverse)

    def set_float(self,add,data,reverse=False):
        if(add>=40000 and add<50000):
            Data=self.WriteFloat(data)
            self.set_int(add,Data[0])
            self.set_int(add+1,Data[1])
            return self.get_float(add)

if __name__=='__main__':
    from machine import UART
    mod=modbus(1,UART(2, baudrate=115200, rx=23, tx=22, timeout=10))
    print(mod.set_int(7,1))
    print(mod.get_int(7))
    print(mod.set_int(9,0))
    print(mod.get_int(11))
    print(mod.set_int(11,1))
    print(mod.get_int(40010))
    print(mod.set_int(40011,666))
    print(mod.get_int(30072))
