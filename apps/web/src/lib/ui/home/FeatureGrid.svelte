<script lang="ts">
	type FeatureItem = {
		title: string;
		description: string;
		kicker?: string;
		href?: string;
	};

	type FeatureGridProps = {
		eyebrow?: string;
		title: string;
		intro?: string;
		items: ReadonlyArray<FeatureItem>;
	};

	let { eyebrow, title, intro, items }: FeatureGridProps = $props();
</script>

<section class="feature-grid">
	<div class="feature-grid__header">
		{#if eyebrow}
			<p class="feature-grid__eyebrow">{eyebrow}</p>
		{/if}

		<h2 class="feature-grid__title">{title}</h2>

		{#if intro}
			<p class="feature-grid__intro">{intro}</p>
		{/if}
	</div>

	<ul class="feature-grid__list">
		{#each items as item}
				<li class="feature-grid__item">
					<article class="feature-card">
						{#if item.kicker}
							<p class="feature-card__kicker">{item.kicker}</p>
						{/if}
						<h3 class="feature-card__title">{item.title}</h3>
						<p class="feature-card__description">{item.description}</p>
						{#if item.href}
							<a class="feature-card__link" href={item.href}>Подробнее</a>
						{/if}
				</article>
			</li>
		{/each}
	</ul>
</section>
