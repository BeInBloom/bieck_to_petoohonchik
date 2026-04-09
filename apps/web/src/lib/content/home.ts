export const homePage = {
	meta: {
		title: 'Pets Board',
		description:
			'Современная доска объявлений о питомцах с typed API и понятным пользовательским контуром.'
	},

	hero: {
		eyebrow: 'Pets Board',
		title: 'Новая доска объявлений о питомцах без устаревшего интерфейса',
		description:
			'Ищи объявления, публикуй свои записи и управляй ими в современном приложении с нормальной архитектурой.',
		primaryAction: {
			label: 'Создать аккаунт',
			href: '/register'
		},
		secondaryAction: {
			label: 'Войти',
			href: '/login'
		},
		stats: [
			{ value: 'API-first', label: 'единый контракт между backend и frontend' },
			{ value: 'Typed', label: 'меньше расхождений в данных' },
			{ value: 'Modular', label: 'страницы собираются из независимых секций' }
		]
	},

	features: {
		eyebrow: 'Что уже заложено',
		title: 'База, на которой можно строить продукт без хаоса',
		intro:
			'Сначала собираем рабочий контур auth и навигации, потом спокойно наращиваем предметные сценарии.',
		items: [
			{
				kicker: 'Auth',
				title: 'Сессионная авторизация',
				description:
					'Регистрация, вход, выход и текущий пользователь работают через backend-controlled cookie flow.'
			},
			{
				kicker: 'Architecture',
				title: 'Разделение UI и данных',
				description:
					'Маршруты, UI-компоненты, API-клиент и контент страницы не смешиваются в один giant component.'
			},
			{
				kicker: 'Contract',
				title: 'Типы из OpenAPI',
				description: 'Frontend не гадает о форме DTO руками и не расходится с backend-моделями.'
			}
		]
	},

	cta: {
		eyebrow: 'Следующий шаг',
		title: 'Подключайся к новому контуру и начинай с базового auth flow',
		description:
			'После этого можно переходить к категориям, объявлениям и защищённым пользовательским действиям.',
		primaryAction: {
			label: 'Перейти к регистрации',
			href: '/register'
		},
		secondaryAction: {
			label: 'У меня уже есть аккаунт',
			href: '/login'
		},
		note: 'Первый рабочий vertical slice важнее, чем десяток полуготовых экранов.'
	}
} as const;
