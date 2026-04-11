export interface paths {
  "/ads": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /** ListAds */
    get: operations["AdsListAds"];
    put?: never;
    /** PostAd */
    post: operations["AdsPostAd"];
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/ads/{id}": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /** GetAd */
    get: operations["AdsIdGetAd"];
    put?: never;
    post?: never;
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/auth/login": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    get?: never;
    put?: never;
    /** Login */
    post: operations["AuthLoginLogin"];
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/auth/logout": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    get?: never;
    put?: never;
    /** Logout */
    post: operations["AuthLogoutLogout"];
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/auth/me": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /** Me */
    get: operations["AuthMeMe"];
    put?: never;
    post?: never;
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/auth/register": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    get?: never;
    put?: never;
    /** Register */
    post: operations["AuthRegisterRegister"];
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/categories": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /** ListCategories */
    get: operations["CategoriesListCategories"];
    put?: never;
    post?: never;
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/categories/{slug}": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /** GetCategory */
    get: operations["CategoriesSlugGetCategory"];
    put?: never;
    post?: never;
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/health": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /** Healthcheck */
    get: operations["HealthHealthcheck"];
    put?: never;
    post?: never;
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/health/db": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /** DbHealthcheck */
    get: operations["HealthDbDbHealthcheck"];
    put?: never;
    post?: never;
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
}
export type webhooks = Record<string, never>;
export interface components {
  schemas: {
    /** AdCreate */
    AdCreate: {
      category_id: number;
      description: string;
      price_minor: number;
      title: string;
    };
    /** AdCreated */
    AdCreated: {
      id: number;
      /** @default ok */
      status: string;
    };
    /** AdRead */
    AdRead: {
      category_id: number;
      /** Format: date-time */
      created_at: string;
      deleted_at?: string | null;
      description: string;
      id: number;
      price_minor: number;
      published_at?: string | null;
      title: string;
      /** Format: date-time */
      updated_at: string;
    };
    /** AdsPageRead */
    AdsPageRead: {
      items: components["schemas"]["AdRead"][];
      limit: number;
      offset: number;
      total: number;
    };
    /** AuthResponse */
    AuthResponse: {
      user: components["schemas"]["UserRead"];
    };
    /** CategoryRead */
    CategoryRead: {
      id: number;
      name: string;
      parent_id?: number | null;
      slug: string;
    };
    /** LoginRequest */
    LoginRequest: {
      /** Format: email */
      email: string;
      password: string;
    };
    /** RegisterRequest */
    RegisterRequest: {
      display_name: string;
      /** Format: email */
      email: string;
      password: string;
    };
    /** UserRead */
    UserRead: {
      /** Format: date-time */
      created_at: string;
      display_name: string;
      /** Format: email */
      email: string;
      id: number;
      is_active: boolean;
      role: components["schemas"]["UserRole"];
      /** Format: date-time */
      updated_at: string;
    };
    /**
     * UserRole
     * @enum {string}
     */
    UserRole: "user" | "staff";
  };
  responses: never;
  parameters: never;
  requestBodies: never;
  headers: never;
  pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
  AdsListAds: {
    parameters: {
      query?: {
        limit?: number;
        offset?: number;
      };
      header?: never;
      path?: never;
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Request fulfilled, document follows */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["AdsPageRead"];
        };
      };
      /** @description Bad request syntax or unsupported method */
      400: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": {
            detail: string;
            extra?:
              | null
              | {
                  [key: string]: unknown;
                }
              | unknown[];
            status_code: number;
          };
        };
      };
    };
  };
  AdsPostAd: {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["AdCreate"];
      };
    };
    responses: {
      /** @description Document created, URL follows */
      201: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["AdCreated"];
        };
      };
      /** @description Bad request syntax or unsupported method */
      400: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": {
            detail: string;
            extra?:
              | null
              | {
                  [key: string]: unknown;
                }
              | unknown[];
            status_code: number;
          };
        };
      };
    };
  };
  AdsIdGetAd: {
    parameters: {
      query?: never;
      header?: never;
      path: {
        id: number;
      };
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Request fulfilled, document follows */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["AdRead"];
        };
      };
      /** @description Bad request syntax or unsupported method */
      400: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": {
            detail: string;
            extra?:
              | null
              | {
                  [key: string]: unknown;
                }
              | unknown[];
            status_code: number;
          };
        };
      };
    };
  };
  AuthLoginLogin: {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["LoginRequest"];
      };
    };
    responses: {
      /** @description Request fulfilled, document follows */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["AuthResponse"];
        };
      };
      /** @description Bad request syntax or unsupported method */
      400: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": {
            detail: string;
            extra?:
              | null
              | {
                  [key: string]: unknown;
                }
              | unknown[];
            status_code: number;
          };
        };
      };
    };
  };
  AuthLogoutLogout: {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Request fulfilled, nothing follows */
      204: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": null;
        };
      };
    };
  };
  AuthMeMe: {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Request fulfilled, document follows */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["UserRead"];
        };
      };
    };
  };
  AuthRegisterRegister: {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["RegisterRequest"];
      };
    };
    responses: {
      /** @description Document created, URL follows */
      201: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["AuthResponse"];
        };
      };
      /** @description Bad request syntax or unsupported method */
      400: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": {
            detail: string;
            extra?:
              | null
              | {
                  [key: string]: unknown;
                }
              | unknown[];
            status_code: number;
          };
        };
      };
    };
  };
  CategoriesListCategories: {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Request fulfilled, document follows */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["CategoryRead"][];
        };
      };
    };
  };
  CategoriesSlugGetCategory: {
    parameters: {
      query?: never;
      header?: never;
      path: {
        slug: string;
      };
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Request fulfilled, document follows */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["CategoryRead"];
        };
      };
      /** @description Bad request syntax or unsupported method */
      400: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": {
            detail: string;
            extra?:
              | null
              | {
                  [key: string]: unknown;
                }
              | unknown[];
            status_code: number;
          };
        };
      };
    };
  };
  HealthHealthcheck: {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Request fulfilled, document follows */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": {
            [key: string]: string;
          };
        };
      };
    };
  };
  HealthDbDbHealthcheck: {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Request fulfilled, document follows */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": {
            [key: string]: string;
          };
        };
      };
    };
  };
}
