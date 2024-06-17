<template>
    <div>
    <LibrarianNavbar></LibrarianNavbar>
    </div>
    <div class="error-message" v-if="error">Sorry! {{ this.error_message }}</div>
    <div class="row">
    <div class="col-md-4"></div>
    <div class="col-md-4">
        <form id="list_form" class="custom-form">
            <div class="mb-3">
                <label for="name" class="form-label">Book Name</label>
                <input type="text" class="form-control" name="listTitle" placeholder="Book Name" v-model="book_info.name">
            </div>
            <div class="mb-3">
                <label for="name" class="form-label">Book Author</label>
                <input type="text" class="form-control" name="listTitle" placeholder="Book Author" v-model="book_info.book_author">
            </div>
            <div class="mb-3">
                <label for="name" class="form-label">Book Link</label>
                <input type="text" class="form-control" name="listTitle" placeholder="Book Link" v-model="book_info.book_link">
            </div>
            <div class="mb-3">
                <label for="description" class="form-label">Book Description</label>
                <textarea class="form-control" name="listDescription" rows="3" maxlength="500" v-model="book_info.content"></textarea>
            </div>
            <button type="submit" v-on:click.prevent="add_book" class="btn btn-primary">Submit</button>
        </form>
    </div>
    <div class="col-md-4"></div>
</div>

</template>
<script>

import axios from 'axios'
import LibrarianNavbar from './LibrarianNavbar.vue'
    export default{
        name: "LibrarianAddBook",
        data() {
            return {
            book_info:{
                name:null,
                content:null,
                book_author:null,
                book_user_id:null,
                book_sec_id:null,
                book_link: null
            },
            token: null,
            error: null,
            error_message: null
            }
        },
        components:{
            LibrarianNavbar
        },
        created() {
            this.book_info.book_sec_id = this.$route.params.sec_id;
        },
        methods:{
            async add_book(){
                try {
                const response = await axios.post(`http://127.0.0.1:5000/api/book`,
                {
                book_name: this.book_info.name,
                book_content: this.book_info.content,
                book_author: this.book_info.book_author,
                book_sec_id: this.book_info.book_sec_id,
                book_user_id: null,
                book_link: this.book_info.book_link
            },
                {
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                console.log(response)
                if (response.status==201) {
                    this.$router.push({ name: 'LibrarianDashboard' })
                } else {
                    throw new Error(response.status);
                }
                } catch (error) {
                console.log(error)
                this.error = error;
                this.error_message = error.response.data.error_message
                }
            }
        },
        async mounted(){
            let user= localStorage.getItem('userInfo');
            if(user!=null){
                this.token = JSON.parse(user).token
            }
            console.log(user)
            if(user==null){
                this.$router.push({name:'LogIn'})
            }
            if (user) {
                let role = JSON.parse(user).role
                if (role == "user") {
                    this.$router.push({ name: 'HomePage' })
                }
                
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

.custom-form {
    max-width: 500px;
    margin: 0 auto;
}

.custom-form .form-label {
    font-weight: bold;
    color: #333;
}

.custom-form .form-control {
    border-radius: 10px;
}

.custom-form button[type="submit"] {
    width: 100%;
}

</style>