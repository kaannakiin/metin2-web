import type { AuthError } from "./auth";

export function authErrorMessage(
  error: AuthError,
  retryAfterSec?: number,
): string {
  switch (error) {
    case "wrong_credentials":
      return "Kullanıcı adı ya da şifre yanlış.";
    case "blocked":
      return "Bu hesap kullanıma kapalı.";
    case "taken":
      return "Bu kullanıcı adı alınmış. Başka bir ad dene.";
    case "captcha":
      return "Doğrulama tamamlanmadı. Kutucuk yenilenince tekrar dene.";
    case "rate_limited":
      return `Çok fazla deneme yapıldı. ${Math.max(1, Math.ceil((retryAfterSec ?? 60) / 60))} dakika sonra tekrar dene.`;
    case "forbidden":
      return "Bu istek kabul edilmedi. Sayfayı yenileyip tekrar dene.";
  }
}

export const NETWORK_ERROR = "Sunucuya ulaşılamadı. Biraz sonra tekrar dene.";
