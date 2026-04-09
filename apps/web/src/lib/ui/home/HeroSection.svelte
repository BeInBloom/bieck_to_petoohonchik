<script lang="ts">
	type ActionLink = {
		label: string;
		href: string;
		variant?: 'primary' | 'secondary';
	};

	type HeroProps = {
		eyebrow?: string;
		title: string;
		description: string;
		primaryAction: ActionLink;
		secondaryAction?: ActionLink;
		stats?: ReadonlyArray<{
			label: string;
			value: string;
		}>;
	};

	let {
		eyebrow,
		title,
		description,
		primaryAction,
		secondaryAction,
		stats = []
	}: HeroProps = $props();
</script>

<section class="hero">
	<div class="hero__content">
		{#if eyebrow}
			<p class="hero__eyebrow">{eyebrow}</p>
		{/if}

		<h1 class="hero__title">{title}</h1>
		<p class="hero__description">{description}</p>

		<div class="hero__actions">
			<a class="hero__button hero__button--primary" href={primaryAction.href}>
				{primaryAction.label}
			</a>

			{#if secondaryAction}
				<a class="hero__button hero__button--secondary" href={secondaryAction.href}>
					{secondaryAction.label}
				</a>
			{/if}
		</div>

		{#if stats.length > 0}
			<ul class="hero__stats">
				{#each stats as stat}
					<li class="hero__stat">
						<strong>{stat.value}</strong>
						<span>{stat.label}</span>
					</li>
				{/each}
			</ul>
		{/if}
	</div>

	<div class="hero__visual" aria-hidden="true">
		<div class="hero__card hero__card--main"></div>
		<div class="hero__card hero__card--accent"></div>
	</div>
</section>
