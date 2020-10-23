<template lang="html">
    <nav class="navbar navbar-expand-md navbar-light bg-light">
        <div class="container">
            <router-link
                    :to="{ name: 'home'}"
                    class="navbar-brand"
            > QuestionPlace
            </router-link>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                    aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item mx-1">
                       <a href="#"></a>
                         <router-link
                                :to="{ name: 'question-editor'}"
                                class="btn btn-sm btn-danger"
                        > Aggiungi domanda
                        </router-link>
                    </li>
                    <li class="nav-item mx-1">
                        <a
                                class="btn btn-sm btn-outline-secondary"
                                href="/accounts/logout/?next=/"
                        > Logout
                        </a>
                    </li>

                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
    export default {
        name: "NavbarComponent"
    }
</script>

<style lang="css">
    .navbar-nav {

    }
    .nav-item {
        border-bottom: 20px;
        margin-bottom: 5px;
    }
    .my-navbar {
        border-bottom: 1px solid #DDD;
    }

    .navbar-brand{
        font-weight: bold;
        font-size: 130%;

    }
    .navbar-brand:hover{
        color: #DC3545 !important;


    }
</style>