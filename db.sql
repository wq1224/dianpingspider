create table dianping
(
  id int auto_increment PRIMARY KEY,
  shopname varchar(100),
  shopurl varchar(300),
  shoplevel varchar(45),
  commentnum varchar(45),
  avgcost VARCHAR(45),
  taste VARCHAR(45),
  envi VARCHAR(45),
  service VARCHAR(45),
  foodtype VARCHAR(45),
  loc VARCHAR(30),
  poi VARCHAR(60),
  addr VARCHAR(150),
  label VARCHAR(300)
 )

update dianping set level=
(case shoplevel 
when '准五星商户' then 4.5
when '四星商户' then 4
when '准四星商户' then 3.5
when '三星商户' then 3
when '二星商户' then 2
when '该商户暂无星级' then 1
else 0 end )