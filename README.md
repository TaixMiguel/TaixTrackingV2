# TaixTrackingV2

<p align="center">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLsF83YwtuOkgdqu3fU2UE5v57k4L_NgWjhw&usqp=CAU" alt="Implementation currently under development"/>
</p>

Aplicación de seguimiento para pedidos de AliExpress

## Notas técnicas
### BBDD
El uso de un gestor de BBDD se trata a través de la librería [dj-database-url](https://pypi.org/project/dj-database-url/).
Por ello, si se desea modificar el gestor se puede utilizar la variable de entorno `DATABASE_URL` para indicar un motor
diferente o simplemente utilizar otra ubicación que no sea la de por defecto.

Por ejemplo, si quisieramos seguir utilizando el gestor SQLite, pero nos gustaría cambiarle de dirección, podríamos 
definir la siguiente variable de entorno con la nueva dirección donde queremos nuestro fichero de BBDD:
> DATABASE_URL=sqlite:////new_path/db.sqlite3
