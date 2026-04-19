<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="app-header">
    <div class="container">
      <h1 class="app-title">Expense Tracker</h1>
      <nav class="app-nav">
        <RouterLink to="/">Dashboard</RouterLink>
        <RouterLink to="/transactions">Transactions</RouterLink>
        <RouterLink to="/categories">Categories</RouterLink>
      </nav>
    </div>
  </header>

  <main class="container app-main">
    <RouterView />
  </main>
</template>

<style scoped>
.app-header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: var(--space-md) 0;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
}

.app-header .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-lg);
}

.app-title {
  font-size: 1.25rem;
  font-weight: 600;
}

.app-nav {
  display: flex;
  gap: var(--space-md);
}

.app-nav a {
  color: var(--color-text-muted);
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-sm);
}

.app-nav a:hover {
  text-decoration: none;
  background: var(--color-bg);
}

/* Vue Router automatycznie dodaje klasę .router-link-active na aktywny link */
.app-nav a.router-link-active {
  color: var(--color-primary);
  font-weight: 500;
}

.app-main {
  padding-top: var(--space-xl);
  padding-bottom: var(--space-xl);
}
</style>