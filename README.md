# micropython_modbus_RTU

#### 介绍
单文件实现micropython读取modbus信息

#### 方法
- get_int(add):获取整形数据，signed
- set_int(add,value):设置整形数据，signed
- get_float(add):获取单精度数据，float CD BA
- get_float(add,True):获取单精度数据，float AB CD
- set_float(add,value):设置单精度数据，float CD BA
- set_float(add,value,True):设置单精度数据，float AB CD

#### 例程
```python
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
```
