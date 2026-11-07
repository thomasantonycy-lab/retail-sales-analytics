#USE online_retail;
#TRUNCATE TABLE online_retail;
#LOAD DATA LOCAL INFILE
#SELECT COUNT(*) AS total_records
#FROM online_retail;

#select * from online_retail where product;
#select description ,unitprice from online_retail where unitprice>100 order by unitprice desc limit 10;
#select description ,unitprice from online_retail where unitprice>50 order by unitprice desc limit 10;
select sum(quantity) as total_quantity from online_retail where quantity >0;
select avg(unitprice) as averageunitprice from online_retail where unitprice>0;
select max(unitprice) as highest_product from online_retail;
select sum(unitprice*quantity) as total_revenue from online_retail where quantity >0;
#1.overall kpi
select round(sum(quantity*unitprice),2) as total_revenue, sum(quantity) as total_quantity, count(distinct invoiceno) as total_orders,count(distinct customerid) as unique_customers,round(avg(unitprice),2) as average_unit from online_retail where quantity > 0;
#2. Revenue by Country
select country, sum(quantity*unitprice) as total_revenue from online_retail where quantity > 0 group by country order by total_revenue desc; 
SELECT StockCode,Description,ROUND(SUM(Quantity * UnitPrice), 2) AS revenue FROM online_retail WHERE Quantity > 0 GROUP BY StockCode, Description ORDER BY revenue DESC LIMIT 10;
#3.Top 10 Customers
select customerid, round(sum(quantity * unitprice),2) as cust_revenue from online_retail where Quantity > 0 and unitprice >=0 and CustomerID!='' group by CustomerID order by cust_revenue desc limit 10;
#4.Monthly Revenue
select date_format(str_to_date(invoicedate, '%d-%m-%Y %H:%i'),'%Y-%m') as sales_month, round(sum(quantity * unitprice),2) as monthly_revenue from online_retail where quantity > 0 and unitprice >=0 group by sales_month order by sales_month;
#5.Top 10 Products
select stockcode,max(description) as product_name, sum(quantity) as total_quantity,round(sum(quantity*unitprice),2)as total_revenue from online_retail where quantity >0 and unitprice >= 0 and description is not NULL and Description !='' group by stockcode order by total_revenue desc limit 10;
#6.Customer Behaviour
select customerid, count(distinct invoiceno) as total_orders, sum(quantity) as total_revenue,round(sum(quantity*unitprice),2) as total_revenue from online_retail where customerid is not NULL and customerid !='' and Quantity >0 and UnitPrice>=0 group by customerid;