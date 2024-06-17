<template>
    <div>
    <LibrarianNavbar></LibrarianNavbar>
    </div>
    <div class="error-message" v-if="error">Sorry! {{ this.error_message }}</div>
    <div class="form-containerr">
    <input type="email" class="form-controll" id="exampleFormControlInput1" placeholder="Find a book" v-model="this.book_namae">
    <button type="submit" class="btn btn-primary" v-on:click="search(this.sec_id, this.book_namae, )">Search</button>
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
            <RouterLink class="nav-link" aria-current="page" :to="{ name: 'LibrarianUpdateBook', params: { book_id: book.book_id } }">
            <button type="button" class="btn btn-primary">Update Book</button>
            </RouterLink>
            <button type="button" class="btn btn-secondary" v-on:click="delete_book(book.book_id)">Delete Book</button>
        </div>
    </div>
</div>
<div class="row">
        <div class="col-4"></div>
        <div class="col-4">
        <span class="center" id="add_list">
            <RouterLink class="nav-link" aria-current="page" :to="{ name: 'LibrarianAddBook', params: { sec_id: this.sec_id } }">
            <img src="https://www.pngkit.com/png/full/670-6706313_plus-button-green.png" alt="add button" width="70" height="70">
            </RouterLink>
        </span>
        </div>
    </div>
    <br><br>
    <h3>Unavailable <small class="text-body-secondary">Books</small></h3>
    <div class="book-container-unavailable">
    <div v-for="book in unavailable_books" :key="book.book_id" class="book-card">
        <div class="book-image">
            <img src="https://img.freepik.com/free-vector/hand-drawn-flat-stack-books_23-2149323628.jpg" width="10" class="card-img-top" alt="Book Cover">
        </div>
        <div class="book-details">
            <h3 class="book-title">{{ book.book_name }}</h3>
            <h4 class="book-author">{{ book.book_author }}</h4>
            <p class="book-content">{{ book.book_content }}</p>
            <div v-for="user in all_users" :key="user.id">
            <h5 class="book-author" v-if="user.id==book.book_user_id">Issued to: {{ user.name }}</h5>
            </div>
            <RouterLink class="nav-link" aria-current="page" :to="{ name: 'LibrarianUpdateBook', params: { book_id: book.book_id } }">
            <button type="button" class="btn btn-primary">Update Book</button>
            </RouterLink>
            <button type="button" class="btn btn-secondary" v-on:click="delete_book(book.book_id)">Delete Book</button>
            <button type="button" class="btn btn-secondary" v-on:click="revoke_book(book.book_id)">Revoke Book Privileges</button>
        </div>
    </div>
</div>
</template>
<script>

import axios from 'axios'
import LibrarianNavbar from './LibrarianNavbar.vue';
    export default{
        name: "LibrarianSecwiseBooks",
        data() {
            return {
            available_books: [],
            unavailable_books: [],
            all_users: [],
            sec_id: null,
            token: null,
            error: null,
            error_message: null,
            book_namae: null
            }
        },
        components:{
            LibrarianNavbar
        },
        created() {
            this.sec_id = this.$route.params.sec_id;
        },
        methods:{
            async delete_book(book_id){
                try{
                let response = await axios.delete(`http://127.0.0.1:5000/api/book/${book_id}`,{
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
                }
        },
        async revoke_book(book_id){
                try{
                let response = await axios.put(`http://127.0.0.1:5000/revoke_book/${book_id}`, {}, {
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
                }
        },
        async search(sec_id, book_name){
            try {
                const response = await axios.get(`http://127.0.0.1:5000/all_books_sectionwise_search/${sec_id}/${book_name}`,{
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
        async mounted(){
            console.log(this.sec_id)
            let user= localStorage.getItem('userInfo');
            if(user!=null){
                this.token = JSON.parse(user).token
            }
            console.log(user)
            if(user==null){
                this.$router.push({name:'SignUp'})
            }
            if (user) {
                let role = JSON.parse(user).role
                console.log(role)
                if (role == "user") {
                    this.$router.push({ name: 'HomePage' })
                }
            }
            try {
                const response = await axios.get(`http://127.0.0.1:5000/all_books_sectionwise/${this.sec_id}`,{
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

                try {
                const response = await axios.get("http://127.0.0.1:5000/all_users",{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                if (response.status==200) {
                    console.log(response.data);
                    this.all_users = response.data;
                    console.log(this.all_users)
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
    opacity: 0.9;
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