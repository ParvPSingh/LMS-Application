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
                <label for="name" class="form-label">Section Name</label>
                <input type="text" class="form-control" name="listTitle" v-model="section_info.name">
            </div>
            <div class="mb-3">
                <label for="description" class="form-label">Section Description</label>
                <textarea class="form-control" name="listDescription" rows="3" maxlength="500" v-model="section_info.description"></textarea>
            </div>
            <button type="submit" v-on:click.prevent="update_section" class="btn btn-primary">Submit</button>
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
            section_info:{
                name:null,
                description:null,
            },
            sec_id: null,
            token: null,
            error: null,
            error_message:null
            }
        },
        components:{
            LibrarianNavbar
        },
        created() {
            this.sec_id = this.$route.params.sec_id;
        },
        methods:{
            async update_section(){
                let user= localStorage.getItem('userInfo');
                if(user){
                    this.section_info.sec_user_id = JSON.parse(user).user_id;
                }
                try {
                const response = await axios.put(`http://127.0.0.1:5000/api/sec/${this.sec_id}`,
                {
                sec_name: this.section_info.name,
                sec_description: this.section_info.description,
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
                const response = await axios.get(`http://127.0.0.1:5000/api/sec/${this.sec_id}`,{
                    headers: {
                        'Authentication-Token': this.token,
                    },
                });
                console.log(response);
                if (response.status==200) {
                    let current_sec = response.data;
                    if(current_sec){
                        this.section_info.name = current_sec.sec_name;
                        this.section_info.description = current_sec.sec_description;
                    }
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