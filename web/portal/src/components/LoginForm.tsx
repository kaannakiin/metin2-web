import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { login } from "../lib/auth";
import { launchGame } from "../lib/launch";
import { NETWORK_ERROR, authErrorMessage } from "../lib/messages";
import { LoginBody } from "../server/validation";
import { Field } from "./Field";
import { FormAlert, SubmitButton } from "./SubmitButton";

export function LoginForm({ defaultLogin }: { defaultLogin?: string }) {
  const [alert, setAlert] = useState<string>();
  const form = useForm<LoginBody>({
    resolver: zodResolver(LoginBody),
    defaultValues: { login: defaultLogin ?? "", password: "" },
  });
  const { errors, isSubmitting } = form.formState;

  const onSubmit = form.handleSubmit(async (values) => {
    setAlert(undefined);
    try {
      const result = await login({ data: values });
      if (result.ok) return launchGame(values.login, values.password);
      setAlert(authErrorMessage(result.error, result.retryAfterSec));
    } catch {
      setAlert(NETWORK_ERROR);
    }
  });

  return (
    <form onSubmit={onSubmit} noValidate className="flex flex-col gap-4">
      <Field
        label="Kullanıcı adı"
        autoComplete="username"
        autoFocus={!defaultLogin}
        error={errors.login && "4–16 harf ya da rakam gir."}
        {...form.register("login")}
      />
      <Field
        label="Şifre"
        type="password"
        autoComplete="current-password"
        autoFocus={!!defaultLogin}
        error={errors.password && "Şifre 6–16 karakter olmalı."}
        {...form.register("password")}
      />
      <FormAlert message={alert} />
      <SubmitButton pending={isSubmitting} idle="Giriş yap ve oyna" busy="Giriş yapılıyor…" />
    </form>
  );
}
