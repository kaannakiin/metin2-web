import { zodResolver } from "@hookform/resolvers/zod";
import { Turnstile, type TurnstileInstance } from "@marsidev/react-turnstile";
import { useRef, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { register as registerAccount } from "../lib/auth";
import { NETWORK_ERROR, authErrorMessage } from "../lib/messages";
import { RegisterBody } from "../server/validation";
import { Field } from "./Field";
import { FormAlert, SubmitButton } from "./SubmitButton";

const RegisterForm_ = RegisterBody.omit({ turnstileToken: true })
  .extend({ passwordAgain: z.string() })
  .refine((v) => v.password === v.passwordAgain, { path: ["passwordAgain"] });

type RegisterValues = z.infer<typeof RegisterForm_>;

export function RegisterForm({
  turnstileSiteKey,
  onRegistered,
}: {
  turnstileSiteKey: string;
  onRegistered: (login: string) => void;
}) {
  const [alert, setAlert] = useState<string>();
  const [token, setToken] = useState<string>();
  const turnstile = useRef<TurnstileInstance>(undefined);
  const form = useForm<RegisterValues>({
    resolver: zodResolver(RegisterForm_),
    defaultValues: {
      login: "",
      password: "",
      passwordAgain: "",
      deleteCode: "",
    },
  });
  const { errors, isSubmitting } = form.formState;

  const onSubmit = form.handleSubmit(
    async ({ passwordAgain: _, ...values }) => {
      if (!token)
        return setAlert("Doğrulama kutucuğunun tamamlanmasını bekle.");
      setAlert(undefined);
      try {
        const result = await registerAccount({
          data: { ...values, turnstileToken: token },
        });
        if (result.ok) return onRegistered(values.login);
        setAlert(authErrorMessage(result.error, result.retryAfterSec));
      } catch {
        setAlert(NETWORK_ERROR);
      }
      setToken(undefined);
      turnstile.current?.reset();
    },
  );

  return (
    <form onSubmit={onSubmit} noValidate className="flex flex-col gap-4">
      <Field
        label="Kullanıcı adı"
        autoComplete="username"
        autoFocus
        hint="4–16 harf ya da rakam. Oyunda bununla giriş yaparsın."
        error={
          errors.login &&
          "4–16 harf ya da rakam gir; Türkçe harf ve boşluk olmasın."
        }
        {...form.register("login")}
      />
      <Field
        label="Şifre"
        type="password"
        autoComplete="new-password"
        hint="6–16 karakter, Türkçe harf ve boşluk olmadan."
        error={
          errors.password && "6–16 karakter gir; Türkçe harf ve boşluk olmasın."
        }
        {...form.register("password")}
      />
      <Field
        label="Şifre tekrar"
        type="password"
        autoComplete="new-password"
        error={errors.passwordAgain && "İki şifre aynı değil."}
        {...form.register("passwordAgain")}
      />
      <Field
        label="Karakter silme kodu"
        inputMode="numeric"
        maxLength={7}
        className="font-mono tracking-[0.3em]"
        hint="7 rakam. Oyunda bir karakteri silerken sorulur."
        error={errors.deleteCode && "Tam 7 rakam gir."}
        {...form.register("deleteCode")}
      />
      <Turnstile
        ref={turnstile}
        siteKey={turnstileSiteKey}
        options={{ theme: "dark", language: "tr", size: "flexible" }}
        onSuccess={setToken}
        onExpire={() => setToken(undefined)}
        onError={() => setToken(undefined)}
      />
      <FormAlert message={alert} />
      <SubmitButton
        pending={isSubmitting}
        idle="Hesap oluştur"
        busy="Hesap oluşturuluyor…"
      />
    </form>
  );
}
