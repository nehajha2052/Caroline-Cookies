# Caroline-Cookies
Database application for inventory management and customer data security for a local bakery shop

Caroline's Cookies Rewards Program is a digital loyalty system designed to replace the store's traditional punch card method. Built with Django, this project allows customers to earn and redeem points for their purchases through an intuitive online platform. It streamlines customer rewards, simplifies inventory management for administrators, and enhances customer engagement by providing a seamless and secure user experience.

## Key Features:

1. User Authentication:

   Secure platform access for customers and administrators using Django's robust authentication system.
2. Point-Based Loyalty Program:
  
   Customers earn points with every purchase, which can be redeemed for rewards like free cookies or discounts.
3. Product Management:

   Admins can manage the store's inventory through the Django admin interface, keeping offerings up-to-date.
4. Order Management:
  
   Efficiently handles customer orders, including tracking history, processing payments, and updating statuses.
5. User Account Management:
  
   Customers can view their purchase history, check loyalty points, and update personal information.
6. Admin Dashboard:
  
   A comprehensive dashboard for administrators to monitor sales, manage user accounts, and track loyalty program performance.

## Tools and Setup
### Tools:

1. Python 3
   
Python serves as the primary programming language for the project, providing a clean and efficient codebase to implement the logic for user authentication, managing database interactions, and handling various backend tasks within the Django framework.

2. Jinja
   
In Caroline's Cookie Tracker, Jinja, a Python templating engine, dynamically generates HTML content within Django templates. It seamlessly integrates Python code for rendering backend data, enhancing the user experience.

3. Django 4:

In this project, Django 4 provides user authentication, URL routing, database management, and HTML template rendering. Its built-in features, like user authentication and ORM, facilitate rapid development and clean design.

4. HTML

In Caroline's Cookie Tracker, HTML structures web pages, working with Jinja templates dynamically rendered by Django to present backend data, creating dynamic and interactive user interfaces.

----
### Schema:
![image](https://github.com/user-attachments/assets/5ae65e44-0f92-498f-b71d-1141c1891be4)

----
### Tables:

|   | Name  |
| :------------ |:---------------:|
| 1      | django_migrations | 
| 2      | django_content_type        | 
| 3      | auth_group_permissions | 
| 4      | auth_permission        | 
| 5      | auth_group | 
| 6      | coupons        | 
| 7      | product_reviews | 
| 8      | purchases        | 
| 9      | user_groups | 
| 10      | user_permissions        | 
| 11      | userpayment | 
| 12      | usercoupons        | 
| 13      | django_admin_log | 
| 14      | django_session        | 
| 15      | cartitem | 
| 16      | cart        | 
| 17      | user | 
| 18      | products        | 


