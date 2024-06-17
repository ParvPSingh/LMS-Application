<template>
    <div>
    <NavBar></NavBar>
    </div>
    <div class="error-message" v-if="error">Sorry! {{ this.error_message }}</div>
    <div class="form-containerr">
    <input type="email" class="form-controll" id="exampleFormControlInput1" placeholder="Find a book" v-model="this.book_namae">
    <button type="submit" class="btn btn-primary" v-on:click="search(this.book_namae)">Search</button>
</div>
    <br>
    <h3>Available <small class="text-body-secondary">Books</small></h3>
    <div class="book-container">
    <div v-for="book in available_books" :key="book.book_id" class="book-card">
        <div class="book-image">
            <img src="https://img.freepik.com/free-vector/hand-drawn-flat-stack-books_23-2149323628.jpg" class="card-img-top" alt="Book Cover">
        </div>
        <div class="book-details">
            <h3 class="book-title">{{ book.book_name }}</h3>
            <h4 class="book-author">{{ book.book_author }}</h4>
            <p class="book-content">{{ book.book_content }}</p>
            <a href="#" class="btn btn-primary" v-on:click="create_request(book.book_id)">Request </a>
        </div>
    </div>
</div>
    <br><br>
    <h3>Unavailable <small class="text-body-secondary">Books</small></h3>
    <div class="book-container-unavailable">
    <div v-for="book in unavailable_books" :key="book.book_id" class="book-card">
        <div class="book-image">
            <img src="https://img.freepik.com/free-vector/hand-drawn-flat-stack-books_23-2149323628.jpg" class="card-img-top" alt="Book Cover">
        </div>
        <div class="book-details">
            <h3 class="book-title">{{ book.book_name }}</h3>
            <h4 class="book-author">{{ book.book_author }}</h4>
            <p class="book-content">{{ book.book_content }}</p>
            <button type="button" class="btn btn-secondary" disabled>Request</button>
        </div>
    </div>
</div>
</template>
<script>

import axios from 'axios'
import NavBar from './NavBar.vue'
    export default{
        name: "HomePage",
        data() {
            return {
            available_books: [],
            unavailable_books: [],
            token: null,
            error: null,
            error_message: null,
            user_id:null,
            book_namae: null
            }
        },
        components:{
            NavBar
        },
        methods:{
            async create_request(boook_id){
                try{
                let response = await axios.post(`http://127.0.0.1:5000/api/req`, {
                    req_user_id : this.user_id,
                    req_book_id : boook_id
                }, {
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                console.log(response)
                if(response.status==200){
                    this.$router.go();
                }
        }
        catch (error) {
                this.error = error;
                console.log(this.error);
                this.error_message = error.response.data.error_message
                }
        },
        async search(book_name){
            try {
                const response = await axios.get(`http://127.0.0.1:5000/all_books_search/${book_name}`,{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                if (response.status==200) {
                    console.log(response.data);
                    this.available_books = response.data[0];
                    this.unavailable_books = response.data[1];
                    console.log(this.available_books)
                } else {
                    throw new Error(response.status);
                }
                } catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
                }
        }
    },
        async created(){
            let user= localStorage.getItem('userInfo');
            if(user!=null){
                this.token = JSON.parse(user).token
                this.user_id = JSON.parse(user).user_id
            }
        }, 
        async mounted(){
            let user= localStorage.getItem('userInfo');
            if(user!=null){
                this.token = JSON.parse(user).token
                this.user_id = JSON.parse(user).user_id
            }
            console.log(user)
            if(user==null){
                this.$router.push({name:'SignUp'})
            }
            if (user) {
                let role = JSON.parse(user).role
                console.log(role)
                if (role == "librarian") {
                    this.$router.push({ name: 'LibrarianDashboard' })
                }
            }
            try {
                const response = await axios.get("http://127.0.0.1:5000/all_books",{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                if (response.status==200) {
                    console.log(response.data);
                    this.available_books = response.data[0];
                    this.unavailable_books = response.data[1];
                    console.log(this.available_books)
                } else {
                    throw new Error(response.status);
                }
                } catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
                }
            
        }
    };
</script>
<style>
.error-message {
    background-color: #f44330;
    color: #fff;
    padding: 10px;
    margin: 0 auto;
    width: 50%;
    text-align: center;
    border-radius: 5px; 
    opacity: 0; 
    animation: fadeIn 0.5s ease forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
.form-containerr {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    width: 100%;
    margin-top: 20px; 
}

.form-controll {
    width: 300px;
    margin-right: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    padding: 8px;
}

.book-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
}

.book-container-unavailable {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    opacity: 0.6;
}

.book-card {
    width: 300px;
    margin: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.book-card:hover {
    transform: translateY(-5px);
}

.book-image {
    text-align: center;
}
</style>