<script lang="ts">
	import type { CurrentUser } from '$lib/api/auth';

	let { user = null }: { user?: CurrentUser | null } = $props();
</script>

<header class="app-header">
	<div class="app-header__inner">
		<div class="app-header__brand-group">
			<a class="app-header__brand" href="/">Pets Board</a>

			<nav class="app-header__nav">
				<a href="/categories">Категории</a>
			</nav>
		</div>

		<div class="app-header__actions">
			{#if user}
				<span class="app-header__user">{user.display_name}</span>
				<a class="app-header__action app-header__action--secondary" href="/account">Профиль</a>
			{:else}
				<a class="app-header__action app-header__action--ghost" href="/login">Войти</a>
				<a class="app-header__action app-header__action--primary" href="/register">Регистрация</a>
			{/if}
		</div>
	</div>
</header>
