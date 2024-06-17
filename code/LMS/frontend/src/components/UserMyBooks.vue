<template>
    <div>
    <NavBar></NavBar>
    </div>
    <div class="error-message" v-if="error">Sorry! {{ this.error_message }}</div>
    <br>
    <h3>My <small class="text-body-secondary">Books</small></h3>
    <div class="book-container">
    <div v-for="book in my_books" :key="book.book_id" class="book-card">
        <a :href="book.book_link">
        <div class="book-image">
            <img src="https://img.freepik.com/free-vector/hand-drawn-flat-stack-books_23-2149323628.jpg" class="card-img-top" alt="Book Cover">
        </div>
        </a>
        <div class="book-details">
            <h3 class="book-title">{{ book.book_name }}</h3>
            <h4 class="book-author">{{ book.book_author }}</h4>
            <p class="book-content">{{ book.book_content }}</p>
            <button type="button" class="btn btn-warning" v-on:click.prevent="return_book(book.book_id)">Return</button>
            <RouterLink class="nav-link" aria-current="page" :to="{ name: 'UserAddFeedback', params: { book_id: book.book_id } }">
            <button type="button" class="btn btn-primary">Add Book Feedback</button>
            </RouterLink>
        </div>
    </div>
</div>
</template>
<script>

import axios from 'axios'
import NavBar from './NavBar.vue'
    export default{
        name: "UserMyBooks",
        data() {
            return {
            my_books: [],
            token: null,
            error: null,
            user_id: null,
            error_message: null,
            }
        },
        components:{
            NavBar
        },
        methods:{
            async return_book(book_id){
                try{
                let response = await axios.put(`http://127.0.0.1:5000/return_book/${book_id}`, {}, {
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
                this.error_message = error.response.data.error_message
                console.error("Error:", error);
            }
        },
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
                if (role == "user") {
                    this.$router.push({ name: 'UserMyBooks' })
                }
                if (role == "librarian") {
                    this.$router.push({ name: 'LibrarianDashboard' })
                }
            }
            try {
                const response = await axios.get(`http://127.0.0.1:5000/my_books/${this.user_id}`,{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                //console.log(response.data);
                //let all_books_data = await response.json();
                //console.log(all_books_data)
                if (response.status==200) {
                    console.log(response.data);
                    this.my_books = response.data;
                    console.log(this.my_books)
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