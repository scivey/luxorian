<template>
    <div class="container-fluid">
        <div class="navbar-logo">
            <img alt="Luxorian Heroes" src="/images/logo.png">
        </div>
        <div class="nav nav-wrapper" id="nav-left">
            <ul class="nav nav-expandable">
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" @click="click-expand" @hover="hover-expand">Play<span class="caret"></span></a>
                    <ul class="dropdown-menu" role="menu" id="play">
                        <li><a href="leagues">Leagues</a></li>
                        <li><a href="teams">Teams</a></li>
                        <li><a href="players">Players</a></li>
                        <li><a href="recruitment">LFG</a></li>
                    </ul>
                </li>
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" @click="click-expand" @hover="hover-expand">Watch<span class="caret"></span></a>
                    <ul class="dropdown-menu" role="menu" id="watch">
                        <li><a href="live">Watch Live</a></li>
                        <li><a href="casting">Casting</a></li>
                        <li><a href="schedule/all">Schedule</a></li>
                    </ul>
                </li>
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" @click="click-expand" @hover="hover-expand">Learn<span class="caret"></span></a>
                    <ul class="dropdown-menu" role="menu" id="learn">
                        <li><a href="stats">Sitewide Hero Statistics</a></li>
                        <li><a href="leaderboard">Leaderboard</a></li>
                        <li><a href="tutorials">Tutorials</a></li>
                        <li><a href="blog">Blog</a></li>
                    </ul>
                </li>
            </ul>
        </div>
        <div class="nav nav-wrapper" id="nav-right">
            <ul class="nav nav-teams">
                <li class="nav-team team-logo"><a href="teams/1"><img alt="Luxorian Sun" src="/images/teams/1.png" /></a></li>
                <li class="nav-team team-logo"><a href="teams/2"><img alt="Luxorian Sand" src="/images/teams/2.png" /></a></li>
                <li class="nav-team team-logo"><a href="teams/3"><img alt="Luxorian Snake" src="/images/teams/3.png" /></a></li>
            </ul>
        </div>
        <div class="nav nav-wrapper" id="nav-user">
            <ul class="nav nav-expandable">
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" @click="click-expand" @hover="hover-expand"><span class="gear"></span></a>
                    <ul class="dropdown-menu" role="menu" id="user-menu">
                        <li><a href="user/profile">My Profile</a></li>
                        <li><a href="user/teams">My Teams</a></li>
                        <li><a href="user/settings">Settings</a></li>
                        <li><a href="user/logout">Logout</a></li>
                        <li><a href="user/profile">Sign in</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>

</script>