<script lang="ts">
	import Button from '$lib/ui/forms/Button.svelte';
	import FormField from '$lib/ui/forms/FormField.svelte';
	import TextField from '$lib/ui/forms/TextField.svelte';
	import PageContainer from '$lib/ui/layout/PageContainer.svelte';
</script>

<PageContainer narrow={true}>
	<section class="login-page">
		<div class="login-panel">
			<header class="login-panel__header">
				<p class="login-panel__eyebrow">Вход</p>
				<h1 class="login-panel__title">Войти в аккаунт</h1>
				<p class="login-panel__description">
					Продолжай работу с объявлениями и пользовательскими действиями.
				</p>
			</header>

			<form class="login-form">
				<FormField id="email" label="Email">
					{#snippet children()}
						<TextField
							id="email"
							name="email"
							type="email"
							placeholder="user@example.com"
							autocomplete="email"
						/>
					{/snippet}
				</FormField>

				<FormField id="password" label="Пароль">
					{#snippet children()}
						<TextField
							id="password"
							name="password"
							type="password"
							placeholder="Введите пароль"
							autocomplete="current-password"
						/>
					{/snippet}
				</FormField>

				<div class="login-form__actions">
					<Button type="submit">Войти</Button>
				</div>
			</form>

			<p class="login-panel__footer">
				Нет аккаунта?
				<a href="/register">Зарегистрироваться</a>
			</p>
		</div>
	</section>
</PageContainer>

<style>
	.login-page {
		padding: 2rem 0 4rem;
	}

	.login-panel {
		display: grid;
		gap: 1.5rem;
		padding: 1.5rem;
		border: 1px solid var(--border);
		border-radius: var(--radius);
		background: var(--surface);
		box-shadow: var(--shadow-sm);
	}

	.login-panel__header {
		display: grid;
		gap: 0.5rem;
	}

	.login-panel__eyebrow {
		margin: 0;
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--primary);
	}

	.login-panel__title {
		margin: 0;
		font-size: clamp(1.75rem, 4vw, 2.25rem);
		line-height: 1.1;
	}

	.login-panel__description {
		margin: 0;
		color: var(--text-muted);
		line-height: 1.5;
	}

	.login-form {
		display: grid;
		gap: 1rem;
	}

	.login-form__actions {
		padding-top: 0.5rem;
	}

	.login-panel__footer {
		margin: 0;
		font-size: 0.95rem;
		color: var(--text-muted);
	}

	.login-panel__footer a {
		color: var(--primary);
		font-weight: 600;
	}

	@media (min-width: 640px) {
		.login-page {
			padding-top: 3rem;
		}

		.login-panel {
			padding: 2rem;
		}
	}
</style>
