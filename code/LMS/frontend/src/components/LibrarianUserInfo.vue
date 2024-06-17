<template>
    <div>
    <LibrarianNavbar></LibrarianNavbar>
    </div>
    <div class="error-message" v-if="error">Sorry! {{ this.error_message }}</div>
    <br>
    <h3>All <small class="text-body-secondary">Users</small></h3>
    <div class="card len" v-for="user in all_users" :key="user.id">
    <h4 class="card-header">{{ user.name }} | {{ user.email }}</h4>
    <div class="card-body">
        <h6 class="card-title">Active Status: {{ user.active }}</h6>
        <p class="card-text">
            <button type="button" class="btn btn-success" v-on:click="activate_user(user.id)">Activate User</button> <button type="button" class="btn btn-danger" v-on:click="revoke_user(user.id)">Revoke User</button></p>
    </div>
    </div>
</template>
<script>

import axios from 'axios'
import LibrarianNavbar from './LibrarianNavbar.vue';
    export default{
        name: "LibrarianUserInfo",
        data() {
            return {
            all_users: [],
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
            async revoke_user(user_id){
                try{
                let response = await axios.put(`http://127.0.0.1:5000/revoke_user/${user_id}`, {}, {
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
                console.error("Error:", error);
            }
        },
        async activate_user(user_id){
                try{
                let response = await axios.put(`http://127.0.0.1:5000/activate_user/${user_id}`, {}, {
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
                const response = await axios.get(`http://127.0.0.1:5000/all_users`,{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                if (response.status==200) {
                    console.log(response.data);
                    this.all_users = response.data;
                    console.log(this.active_requests)
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