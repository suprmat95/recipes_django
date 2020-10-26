<template lang="html">
    <nav class="navbar navbar-expand-md navbar-light bg-light">
        <div class="container">
            <router-link
                    :to="{ name: 'home'}"
                    class="navbar-brand"
            > <b class="navbar-brand">Al.ta Cucina </b>
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
                        >
                            <button class="btn btn-warning">
                                Aggiungi Una Ricetta
                                <md-icon>add</md-icon>

                            </button>

                        </router-link>


                    </li>
                    <li class="nav-item mx-1">
                        <a
                                class="btn btn-secondary color-logout"
                                href="/accounts/logout/"
                                style="color:#DDDDDD;"
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
    .nav-item {
        border-bottom: 20px;
        margin-bottom: 5px;
    }

    .my-navbar {
        border-bottom: 1px solid #DDD;
    }

    .navbar-brand {
        color: goldenrod;
        font-weight: bold;
        font-size: 130%;

    }
    .navbar-brand:hover {
        color: #DC3545 !important;


    }
</style>