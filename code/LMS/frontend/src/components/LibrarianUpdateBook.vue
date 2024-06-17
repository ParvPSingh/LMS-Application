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
                <input type="text" class="form-control" name="listTitle" v-model="book_info.name">
            </div>
            <div class="mb-3">
                <label for="name" class="form-label">Book Author</label>
                <input type="text" class="form-control" name="listTitle" v-model="book_info.book_author">
            </div>
            <div class="mb-3">
                <label for="description" class="form-label">Book Description</label>
                <textarea class="form-control" name="listDescription" rows="3" maxlength="500" v-model="book_info.content"></textarea>
            </div>
            <div class="mb-3">
                <label for="name" class="form-label">Book User ID</label>
                <input type="text" class="form-control" name="listTitle" v-model="book_info.book_user_id">
            </div>
            <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckChecked" checked v-model="book_info.book_available">
                <label class="form-check-label" for="flexSwitchCheckChecked">Book Availability</label>
            </div>
            <select class="form-select" aria-label="Default select example" v-model="book_info.book_sec_id">
                <option selected :value="book_info.book_sec_id">Same Genre</option>
                <option v-for="section in all_sections" :key="section.sec_id" :value="section.sec_id">{{ section.sec_name }}</option>
            </select>
            <button type="submit" v-on:click.prevent="update_book" class="btn btn-primary">Submit</button>
        </form>
    </div>
    <div class="col-md-4"></div>
</div>

</template>
<script>

import axios from 'axios'
import LibrarianNavbar from './LibrarianNavbar.vue'
    export default{
        name: "LibrarianUpdateSection",
        data() {
            return {
            book_info:{
                name:null,
                content:null,
                book_author:null,
                book_available:null,
                book_user_id:null,
                book_sec_id:null,
            },
            all_sections:[],
            sec_id: null,
            book_id:null,
            token: null,
            error: null,
            }
        },
        components:{
            LibrarianNavbar
        },
        created() {
            this.book_id = this.$route.params.book_id;
        },
        methods:{
            async update_book(){
                try {
                const response = await axios.put(`http://127.0.0.1:5000/api/book/${this.book_id}`,
                {
                book_name: this.book_info.name,
                book_author: this.book_info.book_author,
                book_content: this.book_info.content,
                book_available: this.book_info.book_available,
                book_user_id: this.book_info.book_user_id,
                book_sec_id: this.book_info.book_sec_id
            },
                {
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                if (response.status==201) {
                    this.$router.push({ name: 'LibrarianDashboard' })
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
            try {
                const response = await axios.get("http://127.0.0.1:5000/all_sections",{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                if (response.status==200) {
                    this.all_sections = response.data;
                } else {
                    throw new Error(response.status);
                }
                } catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
            }
                try {
                const response = await axios.get(`http://127.0.0.1:5000/api/book/${this.book_id}`,{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                console.log(response);
                if (response.status==200) {
                    let current_book = response.data;
                    if(current_book){
                        this.book_info.name = current_book.book_name;
                        this.book_info.book_author = current_book.book_author;
                        this.book_info.content = current_book.book_content;
                        this.book_info.book_available = current_book.book_available;
                        this.book_info.book_user_id = current_book.book_user_id;
                        this.book_info.book_sec_id = current_book.book_sec_id
                    }
                } else {
                    throw new Error(response.status);
                }
                }catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
            }
                console.log(this.book_info.book_available)
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