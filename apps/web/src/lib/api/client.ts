type Method = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

type ApiClientOption = {
	baseUrl?: string;
	fetch?: typeof fetch;
};

type RequestOptions = {
	method?: Method;
	headers?: HeadersInit;
	body?: unknown;
	signal?: AbortSignal;
};

export class ApiError extends Error {
	readonly status: number;
	readonly payload: unknown;

	constructor(message: string, status: number, payload: unknown) {
		super(message);
		this.name = 'ApiError';
		this.status = status;
		this.payload = payload;
	}
}

export class ApiClient {
	#baseUrl: string;
	#fetch: typeof fetch;

	constructor(option: ApiClientOption = {}) {
		this.#baseUrl = option.baseUrl ?? 'api';
		this.#fetch = option.fetch ?? fetch;
	}

	public async request<T>(path: string, option: RequestOptions = {}): Promise<T> {
		const req = this.createRequest(option);
		const res = await this.#fetch(`${this.#baseUrl}${path}`, req);
		if (!res.ok) await this.handleError(res);
		return (await this.handleResponse(res)) as T;
	}

	public get<T>(path: string, options: Omit<RequestOptions, 'method' | 'body'> = {}): Promise<T> {
		return this.request<T>(path, { ...options, method: 'GET' });
	}

	public post<T>(
		path: string,
		body?: unknown,
		options: Omit<RequestOptions, 'method' | 'body'> = {}
	): Promise<T> {
		return this.request<T>(path, { ...options, method: 'POST', body });
	}

	public delete<T>(
		path: string,
		options: Omit<RequestOptions, 'method' | 'body'> = {}
	): Promise<T> {
		return this.request<T>(path, { ...options, method: 'DELETE' });
	}

	private async handleError(res: Response): Promise<never> {
		const payload = await this.getPayloadByRes(res);
		const message = this.getErrorMessageByPayload(payload);
		throw new ApiError(message, res.status, payload);
	}

	private getErrorMessageByPayload(payload: unknown): string {
		return typeof payload === 'object' && payload !== null && 'detail' in payload
			? String(payload.detail)
			: 'API request failed';
	}

	private async handleResponse(res: Response): Promise<unknown> {
		if (res.status === 204) return undefined;
		return await this.getPayloadByRes(res);
	}

	private async getPayloadByRes(res: Response): Promise<unknown> {
		const contentType = res.headers.get('content-type') ?? '';
		const isJson = contentType.includes('application/json');
		return isJson ? await res.json() : await res.text();
	}

	private createRequest(option: RequestOptions): RequestInit {
		return {
			method: option.method ?? 'GET',
			headers: {
				'content-type': 'application/json',
				...option.headers
			},
			credentials: 'include',
			body: option.body === undefined ? undefined : JSON.stringify(option.body),
			signal: option.signal
		};
	}
}
