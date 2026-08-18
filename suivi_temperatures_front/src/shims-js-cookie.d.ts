declare module 'js-cookie' {
  interface CookieAttributes {
    expires?: number;
    sameSite?: string;
  }

  const Cookies: {
    set(name: string, value: string, attributes?: CookieAttributes): string | undefined;
    get(name: string): string | undefined;
    remove(name: string, attributes?: CookieAttributes): void;
  };

  export default Cookies;
}