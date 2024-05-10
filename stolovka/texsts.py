###################   style   ###################

main_page_style = """
.key{
    width: 100px;
    height: 100px;
    margin: 15px;
    font-size: 50px;
    font-weight: bold;
}

.keyboard{
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    margin: 5%;
    justify-content: center;
    align-items: center;
}

"""

choise_user_page_style = """
body:has(.choise_user){
margin:0px
}
.choise_user{
    max-width:1200px;
    padding:0 15px;
    margin:0px auto;
    
}
.key{
    font-size: 50px;
    display: block; /* Расположить кнопки в виде блоков */
    width: 100%; /* Ширина кнопок равна ширине контейнера */
    padding: 10px 10px 10px 20px; /* Отступы вокруг кнопок */
    margin-bottom: 30px; /* Отступ снизу между кнопками */
    border: 1px solid #ccc; /* Граница кнопок */
    background-color: #f9f9f9; /* Цвет фона кнопок */
    border-radius:50px;
    text-align: left;
    transition:all 0.1s;
}
.key:not(:first-child):active{
    background-color: #8783ab;
     color:white;
     scale:1.1;
     transition:all 0.1s;
    }
    .key:not(:first-child){
     box-shadow: 0 0 10px rgba(0,0,0,0.2);
    }
.key:first-child{
    position: sticky;
    top:0px;
    width: 100%;
    border-radius:0px;}
.key:first-child:active{
    background-color: blue !important;
    color:white;
    transition:all 0.1s;
    }
"""

menu_page_style_advanced = """

      * {
         box-sizing: border-box;
      }

      .menu_table {
        margin-bottom: 40px;
        width: 100%;
        margin:0 auto;
        padding: 10px;
        background-color: #c1c1c1;
        border-radius: 25px;
            tbody {
            flex-direction: column;
            gap: 10px;}
      }
      .dish_column{
        justify-content: space-between;
        align-items: center;
      }
      .dish_column td:first-child{
        min-width: 100px;
        width: 100%;}
      .quantity-control {
         align-items: center !important;
         display: flex !important;
      }

      button {
         border: 1px solid #ccc;
         margin: 0;
         padding: 0;
         outline: none;
         width: 50px;
         height: 50px;
         display: flex;
         justify-content: center;
         align-items: center;
      }
      
      .left-qua {
         border-top-left-radius: 50%;
         border-bottom-left-radius: 50%;
      }

      .counter {
         font-size: 30px;
         text-align: center;
         border: 0px;
         border-top: 1px solid #ccc;
         border-bottom: 1px solid #ccc;
         width: 80px;
         height: 50px;
         line-height: 50px;
      }

      .right-qua {
         border-top-right-radius: 50%;
         border-bottom-right-radius: 50%;
      }
      .left-qua,
      .counter,
      .right-qua{
      cursor:pointer;}

      .dish_name {
        font-size: 28px;
        cursor:pointer;
        padding:9px 5px 9px 15px;
        background-color: #f1f1f1;
        border-radius: 15px;
        transition: all 0.5s;
      }
      .price {
        width:90px;;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align:center;
        padding-top: 5px;
        padding-bottom: 5px;
        padding-right: 5px;
        padding-left: 5px;
        background-color: #fff;
        border-radius: 5px;
        font-size: 20px;
        margin: 0px 15px 0px 50px;
      }



        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #f1f1f1;
        }

        h1 {
            text-align: center;
        }

        p {
            margin: 0;
            padding: 0;
        }

        .wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f1f1f1;
            padding: 20px;
            margin: 0 auto;
            max-width: 1200px;
            width:100%;
        }

        .form {
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }

        .name {
            margin-top: 0px;
            margin-bottom: 6px;
            text-align: center;
            font-size: 40px;
            font-style:italic;
            text-transform:uppercase;
        }

        .item_food {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            align-content: center;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
            background-color: #f1f1f1;
        }

        .text_food {
            margin-right: 10px;
            font-size: 18px;
            font-weight: bold;
        }

        .count_food {
            font-size: 18px;
            font-weight: bold;
            max-width: 100px;
            border: none;
        }

        .sub_food {
            font-size: 18px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            border-top-left-radius: 5px;
            border-bottom-left-radius: 5px;
        }

        .add_food {
            font-size: 18px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
        }

        .price_food {
            margin-right: 10px;
            font-size: 18px;
            font-weight: bold;
        }

        .weight_food {
            margin-right: 10px;
            font-size: 18px;
            font-weight: bold;
        }

        .panel {
            display: flex;
            align-items: center;
        }

        .left_part {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            align-content: center;
            justify-content: flex-start;
            align-items: center;
        }

        .right_part {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            align-content: center;
            justify-content: flex-end;
            align-items: center;
        }

        .result {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            align-content: center;
            justify-content: center;
            align-items: center;
            margin-top: 6px;
        }

        .cancel {
            width: 105px;
            color: white;
            background-color: red;
            font-size: 18px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            border-radius: 5px;
            padding: 10px;
            margin-left: auto;
        }
        
        .previous_dey{
            margin-right: 20px;
            width: 140px;
            color: white;
            background-color: #6b6b6b;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            transition: all 0.1s;
            cursor:pointer;
        }
        .previous_dey:active{
            background-color: #3d0cf7;
            transition: all 0.1s;
        }
        
        .buy {
            width: 85px;
            color: white;
            background-color: #4CAF50;
            font-size: 18px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            border-radius: 5px;
            padding: 10px;
            margin-right: 15px;
        }

        .total_price {
            font-size: 30px;
            font-weight: bold;
            margin-right: 20px;
            text-align: right;
            width: 100%;
            margin-top:10px;
            margin-bottom:10px;
        }
        
        .item_food {
            flex-direction: column;
            align-items: flex-start;
            margin-bottom: 5px;
            padding: 5px;
        }

 
"""

#====# config page #====#

config_page_style = """

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}


.body {
    margin: 0;
}

.content {
    min-width: 850px;
    margin-left: 200px; /* Учитывает ширину боковой панели */
    padding: 0px;
}

/*#####################################*/
/*       Стили полосы прокрутки        */

/* Ширина и цвет полосы прокрутки */
::-webkit-scrollbar {
    width: 10px; /* Ширина полосы прокрутки */
}

/* Стилизация самой полосы */
::-webkit-scrollbar-track {
    background: transparent; /* Цвет фона */
    padding-top: 5px;
    padding-: 5px;
}

/* Стилизация ползунка */
::-webkit-scrollbar-thumb {
    background: #888; /* Цвет ползунка */
    border-radius: 5px;
}

/* Если нужен выпуклый эффект на ползунке */
::-webkit-scrollbar-thumb:hover {
    background: #555; /* Цвет ползунка при наведении */
}

/*#####################################*/
/* Стилизация всплывающего уведомления */

.notification {
    max-width: 600px;
    background-color: rgba(0,40,40, 0.8);
    margin-bottom: 10px;
    font-size: 25px;
    font-weight: bold;
    margin-right: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.2);
    border-radius: 12px;
    padding: 10px;
    bottom: 20px;
    right: 20px;
    min-width: 400px;
    border-left: 12px solid #000;
    border-right: 12px solid #000;
    animation-name: notification;
    animation-duration: 0.5s;
    animation-timing-function: ease-in-out;
}

.notifications {
    color: white;
    font-size: 25px;
    font-weight: bold;
    margin-right: 10px;
    border-radius: 10px;
    padding: 10px;
    position: fixed;
    top: 50%;
    left: 30%;
}

@keyframes notification {
    0% { opacity: 0; }
    100% { opacity: 1; }
}

.notification-animate-to-hide {
    animation-name: notificationToHide;
    animation-duration: 0.5s;
    animation-timing-function: ease-in-out;
}

@keyframes notificationToHide {
    0% { opacity: 1; }
    100% { opacity: 0; }
}


/*#####################################*/
/* Стили бокового меню выбора страницы */
.sub_menu {
    background-color: #c1c1c1;
    width: 90%;
    display: flex;
    flex-direction: column;
    position: relative;
    color: white;
    margin-top: -3px;
}

button {
    padding: 5px 12px;
    border: 1px solid #ccc;
    font-size: 16px;
    background-color: #f8f8f8;
    color: #333;
    cursor: pointer;
    transition: all 0.3s;
    /* Изменяем курсор при наведении */
}

/* Стили для кнопок при наведении */
button:hover {
    transition: all 0.3s;
    background-color: #e0e0e0;
}


button.add-button {
    margin-bottom: 10px;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #008CBA;
    color: white;
    cursor: pointer;
}

button.add-button:hover {
    background-color: #005f79;
}
        
.key {
    background-color: #f0f0f0;
    border: none;
    color: black;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: block;
    width: 90%;
    font-size: 22px;
    margin-top: 10px;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.3s;
}

/* Изменяем стиль кнопки при наведении */
.key:hover {
    color: white;
    background-color: #45a049;
    transition: all 0.3s;
}

.sidebar {
    height: 100%;
    width: 250px;
    position: fixed;
    top: 0;
    left: 0;
    background-color: #111;
    padding-top: 20px;
    display: flex;
    align-items: center;
    flex-direction: column;
}

.sidebar h2 {
    margin: 0px;
    color: white;
    text-align: center;
}

.content {
    margin-left: 250px;
    /* Учитывает ширину боковой панели */
    padding: 0px;
}

"""

define_menu_page_style = """  
.price{
    border-color: #ddd;
    padding: 0px;
    height: 25px;
    width: 60px;
}
    
.price_input{
    width: 60px;
    border-width: 0px;
    padding-left: 4px;
    height: 30px;
}

.menu-container{
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
}

/* Стилизация элемента <input type="week"> */
.week {
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 16px;
    background-color: #f2f2f2;
    color: #333;
}

/* Стили для фокуса */
.week:focus {
    outline: none;
    border-color: #66afe9;
    box-shadow: 0 0 5px rgba(102, 175, 233, 0.6);
}

.heder_button{
    height: 37px;
    margin-left: 10px;
    width: 150px;
    color: white;
    background-color: #4CAF50;
    font-size: 18px;
    font-weight: bold;
    border: none;
    border-radius: 5px;
}

.menu_conteiner{
    padding: 16px;
}

.dish_name{
    border-width: 0px;
    height: 30px;
    width: 310px;
}
            
table {
    flex: none;
    border-collapse: collapse;
    width: 300px;
    margin-top: 20px;
    margin-right: 20px;
}
th, td {
    height: 25px;
    border: 1px solid #ddd;
    padding: 0px;
}
th {
    background-color: #f2f2f2;}
"""

define_ingredients_page_style = """

.edit_last_price{
    margin-left: 10px;
    padding-top: 3px;
    padding-left: 6px;
    padding-right: 6px;
}

.price_input{
    text-align: center;
    border-radius: 10px;
    border: 2px solid #4CAF50;
    font-size: 16px;
    height: 25px;
    width: 80px;
}

.header{
    top: 0px;
    width: 100%;
    height: 50px;
    background-color: #f2f2f2;
    height: 50px;
    display: flex;
}

/************   блок с поиском по таблице и кнопкой добавить   *************/

    .input_ingredient_name{
        weight: 26px;
        padding: 4px;
        border: 2px solid #4CAF50;
        border-bottom-left-radius: 10px;
        border-top-left-radius: 10px;
        font-size: 16px;
        outline: none;
    }

    .add-ingredients-conteiner{
        margin-top: 10px;
        margin-left: 10px;
        height: 32px;
        display: flex;
    }

    .add_ingredient {
        padding: 7px 10px;
        margin-right: 5px;
        border: none;
        border-bottom-right-radius: 10px;
        border-top-right-radius: 10px;
        background-color: #4CAF50;
        color: white;
        cursor: pointer;
    }

    .add_ingredient:hover {background-color: #45a049;}

/*****************************************************/

.ingredients-table-conteiner{
    overflow-x: auto;
    height: calc(100vh - 50px);
}


.table_input_ingredient_name{
    border-width: 0px;
    width: 300px;
    border-radius: 10px;
}

tr:hover {
    background-color: #b5b5b5;
    transition: all 0.5s;
}

input[type="text"] {
    padding: 4px;
    font-size: 16px;
    outline: none;
}

.delete_ingredient {
    padding: 5px 10px;
    margin-right: 5px;
    border: none;
    border-radius: 5px;
    background-color: #af4c4c;
    color: white;
    cursor: pointer;
}

.delete_ingredient:hover {
  background-color: #a04545;
}


table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}

thead th {
    background-color: #f2f2f2;
    border-bottom: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}

tbody td {
    border-bottom: 1px solid #ddd;
    padding: 10px;
}

tbody td[contenteditable="true"] {
    outline: none;
    cursor: pointer;
}

tbody td button {
    padding: 5px 10px;
    margin-right: 5px;
    border: none;
    border-radius: 5px;
    background-color: #4CAF50;
    color: white;
    cursor: pointer;
}

tbody td button:hover {
    background-color: #45a049;
}

.volume_input{
    border: 2px solid #4CAF50;
    border-left-width: 0px;
    border-right-width: 0px;
}

.accept_delete_conteiner{
    position: fixed;
    width: 400px;
    border-radius: 10px;
    border: 2px solid #4CAF50;
    padding: 12px;
    
    top: 15%;
    right: 75px;
    
    box-shadow: 0px 0px 105px 75px;
    
    background-color: #f2f2f2;
}

.delete_action_buttons{
    display: flex;
    width: 100%;
    hight: 40px;
}

.cancel_delete_button{
    color: gray;
    width: 50%;
    height: 30px;
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
    border: 2px solid #a2a2a2;
    background-color: #fafafa;
}

.accept_delete_button{
    color: white;
    width: 50%;
    height: 30px;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
    border: 2px solid #af4c4c;
    background-color: #af4c4c;
}

"""

define_dish_page_style = """
.dish_status{
    width: 65px;
}

.dish_actions{
    width: 350px;
}

.header{
    top: 0px;
    width: 100%;
    height: 50px;
    background-color: #f2f2f2;
    height: 50px;
    display: flex;
}

/************   блок с поиском по таблице и кнопкой добавить   *************/

    .input_dish_name{
        weight: 26px;
        padding: 4px;
        border: 2px solid #4CAF50;
        border-bottom-left-radius: 10px;
        border-top-left-radius: 10px;
        font-size: 16px;
        outline: none;
    }

    .add-dish-conteiner{
        margin-top: 10px;
        margin-left: 10px;
        height: 32px;
        display: flex;
    }

    .add_dish {
        padding: 7px 10px;
        margin-right: 5px;
        border: none;
        border-bottom-right-radius: 10px;
        border-top-right-radius: 10px;
        background-color: #4CAF50;
        color: white;
        cursor: pointer;
    }

    .add_dish:hover {background-color: #45a049;}

/*****************************************************/

.dish_table_conteiner{
    overflow-x: auto;
    height: calc(100vh - 50px);
}

.table_input_dish_name{
    border-width: 0px;
    width: 300px;
    border-radius: 10px;
}

input[type="text"] {
    padding: 4px;
    font-size: 16px;
    outline: none;
}

.delete_dish {
    padding: 5px 10px;
    margin-right: 5px;
    border: none;
    border-radius: 5px;
    background-color: #af4c4c;
    color: white;
    cursor: pointer;
}

.delete_dish:hover {
  background-color: #a04545;
}

tr:hover {
    background-color: #b5b5b5;
    transition: all 0.5s;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}

thead th {
    background-color: #f2f2f2;
    border-bottom: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}

tbody td {
    border-bottom: 1px solid #ddd;
    padding: 10px;
}

tbody td[contenteditable="true"] {
    outline: none;
    cursor: pointer;
}

tbody td button {
    padding: 5px 10px;
    margin-right: 5px;
    border: none;
    border-radius: 5px;
    background-color: #4CAF50;
    color: white;
    cursor: pointer;
}

tbody td button:hover {
    background-color: #45a049;
}

/************   блок с рецептами блюд   *************/
 
.recipe_conteiner{
    min-width: 700px;
    position: fixed;
    height: 500px;
    border-radius: 10px;
    border: 2px solid #4CAF50;
    
    top: 15%;
    left: 325px;
    right: 75px;
    
    box-shadow: 0px 0px 105px 75px;
    
    background-color: #f2f2f2;
}

.recipe_conteiner_header{
    border: 2px solid #4CAF50;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
    background: #878787;
    display: flex;
}

.recipe_conteiner_body{
    height: 456.6px;
    overflow-x: auto;
}

.close_recipe{
    width: 200px;
    margin-top: 4px;
    margin-bottom: 4px;
    margin-right: 12px;
    border: 2px solid #af4c4c;
    color: white;
    border-radius: 10px;
    background-color: #af4c4c;
}

.add-ingredients-conteiner{
    display: flex;

    margin-left: 3px;
    margin-top: 4px;
    margin-bottom: 4px;
}

.add_ingredient{
    border: 2px solid #4CAF50;
    color: white;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
    background-color: #4CAF50;
}

.add_ingredient_select{
    border: 2px solid #4CAF50;
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
    background-color: #f2f2f2;
    width: 200px;
}

.input{
    border: 2px solid #4CAF50;
    border-radius: 10px;
    background-color: #f2f2f2;
    height: 20px;
    width: 60px;
}

.padding_4{
    padding: 4px;
}

.delete_ingredient{
    border: 2px solid #af4c4c;
    color: white;
    border-radius: 10px;
    background-color: #af4c4c;
}

.delete_ingredient:hover{
    background-color: #a04545;
}

.close_recipe:hover{
    background-color: #a04545;
}

.ingredients_actions{
    width: 100px;
    padding: 4px;
}

.set_volume{
    font-size: 14px;
    margin-left: 10px;
    padding-left: 6px;
    padding-right: 6px;
    padding-bottom: 3px;
    padding-top: 1px;
}

.input_volume{
    width: 150px;
    padding: 4px;
}

.dish_name{
    color: #f1f1f1;
    margin: 0px;
    margin-left: 10px;
}

"""

control_user_page_style = """

.user_status{
    width: 65px;
}

.user_actions{
    width: 250px;
}

.header{
    top: 0px;
    width: 100%;
    height: 50px;
    background-color: #f2f2f2;
    height: 50px;
    display: flex;
}

/************   блок с поиском по таблице и кнопкой добавить   *************/

    .input_user_name{
        weight: 26px;
        padding: 4px;
        border: 2px solid #4CAF50;
        border-bottom-left-radius: 10px;
        border-top-left-radius: 10px;
        font-size: 16px;
        outline: none;
    }

    .add-user-conteiner{
        margin-top: 10px;
        margin-left: 10px;
        height: 32px;
        display: flex;
    }

    .add_user {
        padding: 7px 10px;
        margin-right: 5px;
        border: none;
        border-bottom-right-radius: 10px;
        border-top-right-radius: 10px;
        background-color: #4CAF50;
        color: white;
        cursor: pointer;
    }

    .add_user:hover {background-color: #45a049;}

/*****************************************************/

.users-table-conteiner{
    overflow-x: auto;
    height: calc(100vh - 50px);
}

.table_input_user_name{
    border-width: 0px;
    width: 300px;
    border-radius: 10px;
}

input[type="text"] {
    padding: 4px;
    font-size: 16px;
    outline: none;
}

.delete_user {
    padding: 5px 10px;
    margin-right: 5px;
    border: none;
    border-radius: 5px;
    background-color: #af4c4c;
    color: white;
    cursor: pointer;
}

.delete_user:hover {
  background-color: #a04545;
}

tr:hover {
    background-color: #b5b5b5;
    transition: all 0.5s;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}

thead th {
    background-color: #f2f2f2;
    border-bottom: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}

tbody td {
    border-bottom: 1px solid #ddd;
    padding: 10px;
}

tbody td[contenteditable="true"] {
    outline: none;
    cursor: pointer;
}

tbody td button {
    padding: 5px 10px;
    margin-right: 5px;
    border: none;
    border-radius: 5px;
    background-color: #4CAF50;
    color: white;
    cursor: pointer;
}

tbody td button:hover {
    background-color: #45a049;
}

"""

###################   scripts   ###################

scripts_for_menu = """
function UpdateMenu() {

    function GetTableData(table_id){
        var table = document.getElementById(table_id);
        var rows = table.querySelectorAll("tr");
        
        var dey_menu = {};
    
        for (var i = 1; i < rows.length; i++) {
            var select = rows[i].querySelector("select");
            var selectedValue = select.value;
            var input = rows[i].querySelector("input");
            var price = input.value;
            
            dey_menu["name" + i] = selectedValue;
            dey_menu["price" + i] = price;
            
        }
        
        return dey_menu;
    }
    
    menuData = [GetTableData("dey1"), GetTableData("dey2"), GetTableData("dey3"), GetTableData("dey4"), GetTableData("dey5")];


    
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
   
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "Memu";
    input.value = JSON.stringify(menuData);
   
    var input1 = document.createElement("input");
    input1.type = "hidden";
    input1.name = "Week";
    input1.value = document.getElementById("week").value;
    
    form.appendChild(input1);
    form.appendChild(input);
    
    document.body.appendChild(form);
    form.submit();
}

        
function WeekChange() {
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
   
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "GetMemu";
    input.value = document.getElementById("week").value;
   
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

function PriceRecalculate(){
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере

    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "PriceRecalculate";
    input.value = document.getElementById("week").value;
   
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

"""

scripts_for_users = """

function FilterUserList() {
    var filter = document.getElementById('newUserName').value.toLowerCase();
    
    const userColumns = document.getElementsByClassName('user_column');

    if (filter === '') {
        for (let i = 0; i < userColumns.length; i++) {userColumns[i].style.display = 'table-row';}
    } else {
        for (let i = 0; i < userColumns.length; i++) {
            const input = userColumns[i].querySelector('input');
            const text = input.value.toLowerCase();
            if (text.includes(filter)){
                userColumns[i].style.display = 'table-row';
            } else {
                userColumns[i].style.display = 'none';
            }
        }
    }
}

function ChangeUserStatus(id) {
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи значения
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "ChangeUserStatus";
    input.value = id;

    // Добавляем элемент input к форме
    form.appendChild(input);
  
    document.body.appendChild(form);
    form.submit();
}

function DeleteUser(id) {
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи значения
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "DeleteUser";
    input.value = id;

    // Добавляем элемент input к форме
    form.appendChild(input);
  
    document.body.appendChild(form);
    form.submit();
}

function EditUserName(id){
    // Получаем содержимое поля ввода
    var newUserName = document.getElementById('UserName'+id).value;
            
    // Проверяем, не является ли поле ввода пустым
    if (newUserName.trim() === '') {

    const notification = new NotificationCustom('Ошибка','Имя пользователя не может быть пустым');
    notification.show();
    return;}
  
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи нового имени пользователя
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "EditUserName";
    input.value = newUserName;
    form.appendChild(input);
            
            
    // Создаем элемент input1 для передачи id пользователя
    var input1 = document.createElement("input");
    input1.type = "hidden";
    input1.name = "id";
    input1.value = id;
    form.appendChild(input1);
  
    document.body.appendChild(form);
    form.submit();
}

function NewUser() {
    // Получаем содержимое поля ввода
    var newUserName = document.getElementById('newUserName').value;
            
    // Проверяем, не является ли поле ввода пустым
    if (newUserName.trim() === '') {
        alert('Имя пользователя не может быть пустым');
        return; // Прерываем выполнение функции
    }
  
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи значения
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "NewUser";
    input.value = newUserName;
    form.appendChild(input);

    // Очищаем поле ввода после добавления пользователя
    document.getElementById('newUserName').value = '';
  
    document.body.appendChild(form);
    form.submit();
}

function showEditButton(userId) {
    var editButton = document.getElementById("editButton" + userId);
    editButton.style.display = "inline-block"; // Показываем кнопку
}

function hideEditButton(userId) {
    var editButton = document.getElementById("editButton" + userId);
    editButton.style.display = "none"; // Скрываем кнопку
}

function hideEditButtonWithDelay(userId) {
    setTimeout(function() {hideEditButton(userId);}, 300);
}

"""

config_page_scripts = """

//#####################################
// JS для всплывающего уведомления


class NotificationCustom {
    constructor(title, message, type = 'push') {
        this.title = title;
        this.message = message;
        this.type = type;
    }

    show() {
        const container = document.createElement('div');
        container.classList.add('notification');

        const title = document.createElement('h3');
        title.classList.add('title');
        title.innerText = this.title;

        const message = document.createElement('p');
        message.classList.add('message');
        message.innerText = this.message;

        container.append(title, message);
        document.querySelector('.notifications').append(container);

        setTimeout(() => {
            container.classList.add('notification-animate-to-hide');
            container.remove();
        }, 3000);
    }
}

//#####################################




function openpage(key) {
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере

    // Создаем элемент input для передачи значения
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "Page";
    input.value = key;
    form.appendChild(input);
    
    document.body.appendChild(form);
    form.submit();
}
"""

main_page_scripts = """

function letter(key){
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = ""; // Укажите здесь путь к вашему обработчику на сервере

    // Создаем элемент input для передачи значения
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "letter";
    input.value = key;
    form.appendChild(input);
    
    document.body.appendChild(form);
    form.submit();
}

"""

choise_user_page_scripts = """

function chose_menu(id){
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = ""; // Укажите здесь путь к вашему обработчику на сервере

    // Создаем элемент input для передачи значения
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "user";
    input.value = id;
    form.appendChild(input);
    
    document.body.appendChild(form);
    form.submit();
}

function PreviousDay(){
    window.history.back();
}
"""

menu_page_scripts = """

var aktive_dey = "0";

document.addEventListener('DOMContentLoaded', function() {
    menu_filling();
});

function menu_filling() {

    let columns = [];
    for (let i = 1; i <= 8; i++) {
        var column = document.getElementById("dish_column_" + i);
        column.style.display = 'none';
        columns.push(column);}

    let data = [];
        
    if (aktive_dey === "0") {
        data = today_data;
    } else {
        data = previous_dey_data;
    }

    let dish_list = [];
    for (let i = 1; i <= 8; i++) {if (data["name" + i] !== "") {dish_list.push([data["name" + i], data["price" + i]]);}}
        
    for (let i = 0; i < dish_list.length; i++) {
        columns[i].style.display = 'table-row';
            
        document.getElementById("dish_name" + (i+1)).innerText = dish_list[i][0];
        document.getElementById("dish_price" + (i+1)).innerText = dish_list[i][1] + " Грн";
    }
            
}

function swech_dey() {
    var button = document.getElementById("previous_dey");
    if (aktive_dey === "0") {
        button.innerText = "Текущий день";
        aktive_dey = "1";
    } else {
        button.innerText = "Предыдущий день";
        aktive_dey = "0";
    }
    
    for (let i = 1; i <= 8; i++) {
        document.getElementById("quantity" + i).value = 0;
    }
    
    total_price_resume()
    menu_filling()
}

function buy() {
    
    let basket = []
    for (let i = 1; i <= 8; i++) {
        var dish_name = document.getElementById("dish_name" + i).textContent;
        var dish_price = document.getElementById("dish_price" + i).textContent.slice(0, -4);
        var quantity = document.getElementById("quantity" + i).value;
        basket.push([dish_name, [dish_price, quantity]]);
    }
    
    const userNameElement = document.getElementById('user_name');
    const userName = userNameElement.textContent;
    
    var form = document.createElement("form");
    form.method = "POST";
    form.action = "";
    
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "order";
    input.value = JSON.stringify({'userName':userName, 'order':basket});

    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

function total_price_resume() {

    let basket = []
    for (let i = 1; i <= 8; i++) {
        var dish_price = document.getElementById("dish_price" + i).textContent.slice(0, -4);
        var quantity = document.getElementById("quantity" + i).value;
        basket.push([dish_price, quantity]);}
        
    let total_price = 0;
    for (let i = 0; i < basket.length; i++) {
        total_price += basket[i][0] * basket[i][1];
    }
    
    var total_price_item = document.getElementById("total_price");
    total_price_item.innerText = "Всего: " + total_price + "грн";
}

function increment(index) {
    var inputElement = document.getElementById("quantity" + index);
    var value = parseInt(inputElement.value, 10);
    inputElement.value = value + 1;
    total_price_resume()
}

function decrement(index) {
    var inputElement = document.getElementById("quantity" + index);
    var value = parseInt(inputElement.value, 10);
    if (value > 0) {
        inputElement.value = value - 1;
        total_price_resume()
    }
}

function PreviousDay(){
    window.history.back();
}
"""

scripts_for_dish_page = """

function FilterDishList() {
    var filter = document.getElementById('newDishName').value.toLowerCase();
    const dishColumns = document.getElementsByClassName('dish_column');

    if (filter === '') {
        for (let i = 0; i < dishColumns.length; i++) {dishColumns[i].style.display = 'table-row';}
    } else {
        for (let i = 0; i < dishColumns.length; i++) {
            const input = dishColumns[i].querySelector('input');
            const inputValue = input.value.toLowerCase();
            if (inputValue.includes(filter)){
                dishColumns[i].style.display = 'table-row';
            } else {
                dishColumns[i].style.display = 'none';
            }
        }
    }
}

function ChangeDishStatus(id) {
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи значения
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "ChangeDishStatus";
    input.value = id;

    // Добавляем элемент input к форме
    form.appendChild(input);
  
    document.body.appendChild(form);
    form.submit();
}

function DeleteDish(id) {
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи значения
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "DeleteDish";
    input.value = id;

    // Добавляем элемент input к форме
    form.appendChild(input);
  
    document.body.appendChild(form);
    form.submit();
}

function EditDishName(id){
    // Получаем содержимое поля ввода
    var newDishName = document.getElementById('DishName'+id).value;
            
    // Проверяем, не является ли поле ввода пустым
    if (newDishName.trim() === '') {

    const notification = new NotificationCustom('Ошибка','Имя пользователя не может быть пустым');
    notification.show();
    return;}
  
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи нового имени пользователя
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "EditDishName";
    input.value = newDishName;
    form.appendChild(input);
            
            
    // Создаем элемент input1 для передачи id пользователя
    var input1 = document.createElement("input");
    input1.type = "hidden";
    input1.name = "id";
    input1.value = id;
    form.appendChild(input1);
  
    document.body.appendChild(form);
    form.submit();
}

function NewDish() {
    // Получаем содержимое поля ввода
    var newDishName = document.getElementById('newDishName').value;
            
    // Проверяем, не является ли поле ввода пустым
    if (newDishName.trim() === '') {
        alert('Имя пользователя не может быть пустым');
        return; // Прерываем выполнение функции
    }
  
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи значения
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "NewDish";
    input.value = newDishName;
    form.appendChild(input);

    // Очищаем поле ввода после добавления пользователя
    document.getElementById('newDishName').value = '';
  
    document.body.appendChild(form);
    form.submit();
}

/////////////////// Функционал редактирования рецептов

function Recipe(id){
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи значения
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "Recipe";
    input.value = id;
    form.appendChild(input);

    document.body.appendChild(form);
    form.submit();
}

function СloseRecipeWindow() {
    document.getElementById('recipeWindow').style.display = 'none';
}

function UpdateRecipe(id) {
    var IngredientId = document.getElementById('newIngredient').value;

    if (IngredientId === '') {
    const notification = new NotificationCustom('Ошибка','Выберите ингредиент, который хотите добавить в рецепт');
    notification.show();
    return;}

    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи значения ингридиента
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "AddIngredientToRecipe";
    input.name = "AddIngredientToRecipe";
    input.value = IngredientId;
    form.appendChild(input);
    
    // Создаем элемент input1 для передачи id блюда
    var input1 = document.createElement("input");
    input1.type = "hidden";
    input1.name = "DishId";
    input1.value = id;
    form.appendChild(input1);
  
    document.body.appendChild(form);
    form.submit();
    
}

function DeleteIngredientFromRecipe (DishId, IngredientId) {
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи значения ингридиента
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "DeleteIngredientFromRecipe";
    input.value = IngredientId;
    form.appendChild(input);
    
    // Создаем элемент input1 для передачи id блюда
    var input1 = document.createElement("input");
    input1.type = "hidden";
    input1.name = "DishId";
    input1.value = DishId;
    form.appendChild(input1);
  
    document.body.appendChild(form);
    form.submit();
}

function SaveVolume(DishId, IngredientId) {
    var Volume = document.getElementById('set_ingridient_volume' + IngredientId).value;

    if (Volume === '') {
    const notification = new NotificationCustom('Ошибка','Введите объем ингредиента');
    notification.show();
    return;}
    
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи id блюда
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "IngredientVolumeData";
    input.value = JSON.stringify({'IngredientId':IngredientId, 'Volume':Volume});
    form.appendChild(input);
    
    // Создаем элемент input1 для передачи значения
    var input1 = document.createElement("input");
    input1.type = "hidden";
    input1.name = "DishId";
    input1.value = DishId;
    form.appendChild(input1);
  
    document.body.appendChild(form);
    form.submit();
}

function showIngredientVolumeEditButton(dishId) {
    var editButton = document.getElementById("set_volume" + dishId);
    editButton.style.display = "inline-block"; // Показываем кнопку
}

function hideIngredientVolumeEditButton(dishId) {
    var editButton = document.getElementById("set_volume" + dishId);
    editButton.style.display = "none"; // Скрываем кнопку
}

function hideIngredientVolumeEditButtonWithDelay(dishId) {
    setTimeout(function() {hideIngredientVolumeEditButton(dishId);}, 300);
}

///////////////////

function showEditButton(dishId) {
    var editButton = document.getElementById("editButton" + dishId);
    editButton.style.display = "inline-block"; // Показываем кнопку
}

function hideEditButton(dishId) {
    var editButton = document.getElementById("editButton" + dishId);
    editButton.style.display = "none"; // Скрываем кнопку
}

function hideEditButtonWithDelay(dishId) {
    setTimeout(function() {hideEditButton(dishId);}, 300);
}

"""

scripts_for_ingredients_page = """
function FilterIngredientList() {
    var filter = document.getElementById('newIngredientName').value.toLowerCase();
    
    const ingredientColumns = document.getElementsByClassName('ingredients_column');

    if (filter === '') {
        for (let i = 0; i < ingredientColumns.length; i++) {ingredientColumns[i].style.display = 'table-row';}
    } else {
        for (let i = 0; i < ingredientColumns.length; i++) {
            const input = ingredientColumns[i].querySelector('input');
            const text = input.value.toLowerCase();
            if (text.includes(filter)){
                ingredientColumns[i].style.display = 'table-row';
            } else {
                ingredientColumns[i].style.display = 'none';
            }
        }
    }
}

function DeleteIngredient() {
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
            
    // Создаем элемент input для передачи значения
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "DeleteIngredient";
    input.value = IngredientToDelete;

    // Добавляем элемент input к форме
    form.appendChild(input);
  
    document.body.appendChild(form);
    form.submit();
}

function EditIngredientName(id){
    // Получаем содержимое поля ввода
    var newIngredientName = document.getElementById('IngredientName'+id).value;
    
    // Проверяем, не является ли поле ввода пустым
    if (newIngredientName.trim() === '') {

    const notification = new NotificationCustom('Ошибка','Название ингридиента не может быть пустым');
    notification.show();
    return;}
    
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
    
    // Создаем элемент input для передачи нового имени пользователя
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "EditIngredientName";
    input.value = newIngredientName;
    form.appendChild(input);
    
    // Создаем элемент input1 для передачи id пользователя
    var input1 = document.createElement("input");
    input1.type = "hidden";
    input1.name = "id";
    input1.value = id;
    form.appendChild(input1);
    
    // Очищаем поле ввода после добавления пользователя
    document.getElementById('newIngredientName').value = '';
  
    document.body.appendChild(form);
    form.submit();
}

function NewIngredient() {
    // Получаем содержимое поля ввода
    var newIngredientName = document.getElementById('newIngredientName').value;
            
    // Проверяем, не является ли поле ввода пустым
    if (newIngredientName.trim() === '') {
        alert('Название ингридиента не может быть пустым');
        return; // Прерываем выполнение функции
    }
    
    var newIngredientVolume = document.getElementById('newIngredientVolume').value;
    
    if (newIngredientVolume === '') {
        alert('Выберете единицу учёта для продукта');
        return; // Прерываем выполнение функции
    }
  
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
    
    // Создаем элемент input1 для передачи значения
    var input1 = document.createElement("input");
    input1.type = "hidden";
    input1.name = "NewIngredientVolume";
    input1.value = newIngredientVolume;
    form.appendChild(input1);
    
    // Создаем элемент input для передачи значения
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "NewIngredientName";
    input.value = newIngredientName;
    form.appendChild(input);
  
    document.body.appendChild(form);
    form.submit();
}

function editLastPrice(id){
    // Получаем содержимое поля ввода
    var LastPrice = document.getElementById('newLastPrice'+id).value;
    
    console.log(LastPrice)
    
    // Проверяем, не является ли поле ввода пустым
    if (LastPrice.trim() === '') {

    const notification = new NotificationCustom('Ошибка','Введите цену ингредиента');
    notification.show();
    return;}
    
    var form = document.createElement("form"); // Создаем объект формы
    form.method = "POST"; // Устанавливаем метод POST
    form.action = "/config"; // Укажите здесь путь к вашему обработчику на сервере
    
    // Создаем элемент input для передачи новой цены ингредиента
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "LastPrice";
    input.value = LastPrice;
    form.appendChild(input);
    
    // Создаем элемент input1 для передачи id пользователя
    var input1 = document.createElement("input");
    input1.type = "hidden";
    input1.name = "id";
    input1.value = id;
    form.appendChild(input1);
  
    document.body.appendChild(form);
    form.submit();
}

var IngredientToDelete = 0;

function DeleteIngredientDiolog(IngredientID){
    IngredientToDelete = IngredientID;
    
    document.getElementById("accept_delete_conteiner").style.display = 'block';
}

function cancelDelete(){
    document.getElementById("accept_delete_conteiner").style.display = 'none';
}

//////////////////////

function showEditButton(ingredientId) {
    var editButton = document.getElementById("editButton" + ingredientId);
    editButton.style.display = "inline-block"; // Показываем кнопку
}

function hideEditButton(ingredientId) {
    var editButton = document.getElementById("editButton" + ingredientId);
    editButton.style.display = "none"; // Скрываем кнопку
}

function showEditLastPriceButton(ingredientId) {
    var editButton = document.getElementById("editLastPrice" + ingredientId);
    editButton.style.display = "inline-block"; // Показываем кнопку
}

function hideEditLastPriceButton(ingredientId) {
    var editButton = document.getElementById("editLastPrice" + ingredientId);
    editButton.style.display = "none"; // Скрываем кнопку
}

function hideEditButtonWithDelay(ingredientId) {
    setTimeout(function() {hideEditButton(ingredientId);}, 300);
}

function hideEditLastPriceButtonWithDelay(ingredientId) {
    setTimeout(function() {hideEditLastPriceButton(ingredientId);}, 300);
}
"""