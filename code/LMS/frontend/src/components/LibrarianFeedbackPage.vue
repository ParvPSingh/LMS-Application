<template>
    <div>
    <LibrarianNavbar></LibrarianNavbar>
    </div>
    <div class="error-message" v-if="error">Sorry! {{ this.error_message }}</div>
    <br>
    <h3>All <small class="text-body-secondary">Feedback</small></h3>
    <div class="card len" v-for="feed in feedbacks" :key="feed.feed_id">
    <h4 class="card-header">{{ feed.book_name }} | {{ feed.user_name }}</h4>
    <div class="card-body">
        <h4 class="card-title">Rating : {{ feed.rating }}</h4>
        <h5>{{ feed.content }}</h5>
        <p class="card-text">
            <button type="button" class="btn btn-danger" v-on:click="delete_feedback(feed.feed_id)">Delete Feedback</button></p>
    </div>
    </div>
</template>
<script>

import axios from 'axios'
import LibrarianNavbar from './LibrarianNavbar.vue';
    export default{
        name: "LibrarianFeedbackPage",
        data() {
            return {
            feedbacks: [],
            sec_id: null,
            token: null,
            error: null,
            error_message: null,
            }
        },
        components:{
            LibrarianNavbar
        },
        methods:{
            async delete_feedback(feed_id){
                try{
                let response = await axios.delete(`http://127.0.0.1:5000/api/feed/${feed_id}`,{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                console.log(response)
                if(response.status==200){
                    this.$router.go();
                }
                else {
                    throw new Error(response.status);
                }
        }
        catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
                }
        },
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
                const response = await axios.get(`http://127.0.0.1:5000/all_feedback`,{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                if (response.status==200) {
                    console.log(response.data);
                    this.feedbacks = response.data;
                    console.log(this.active_requests)
                } else {
                    throw new Error(response.status);
                }
                }catch (error) {
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
.len{
    width:95%;
    margin: 30px;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;    
}

.len:hover{
    transform: translateY(-5px);
}

.opaque{
    opacity: 0.6;
}
</style>