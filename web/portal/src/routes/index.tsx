import { Link, createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { LoginForm } from "../components/LoginForm";
import { MetinStone } from "../components/MetinStone";
import { RegisterForm } from "../components/RegisterForm";
import { getPublicConfig } from "../lib/public-config";
import { SITE } from "../site";

type Tab = "giris" | "kayit";

export const Route = createFileRoute("/")({
  validateSearch: (search): { tab?: "kayit" } =>
    search.tab === "kayit" ? { tab: "kayit" } : {},
  loader: () => getPublicConfig(),
  component: Home,
});

function Home() {
  const tab: Tab = Route.useSearch().tab ?? "giris";
  const { turnstileSiteKey } = Route.useLoaderData();
  const navigate = Route.useNavigate();
  const [registeredLogin, setRegisteredLogin] = useState<string>();

  return (
    <main className="relative isolate flex min-h-dvh flex-col items-center overflow-hidden bg-[radial-gradient(90%_60%_at_50%_0%,#22265a_0%,#0b1530_60%)] px-4 py-12 lg:flex-row lg:justify-center lg:gap-24 lg:px-12">
      <Ridge />

      <header className="mb-12 max-w-md text-center lg:mb-0 lg:text-left">
        <h1 className="font-display text-6xl font-extrabold tracking-tight text-gold sm:text-7xl">
          {SITE.name}
        </h1>
        <p className="mt-5 text-lg leading-relaxed text-rice/90">
          Tarayıcında açılır, kurulum gerekmez.
        </p>
        <p className="mt-2 text-sm text-mist">
          Hesabını oluştur, giriş yap; oyun aynı sekmede başlar.
        </p>
      </header>

      <section
        className="w-full max-w-105"
        aria-label={tab === "giris" ? "Giriş yap" : "Hesap oluştur"}
      >
        <MetinStone>
          <nav className="mb-7 grid grid-cols-2 border-b border-gold/20 text-center font-display text-[17px] font-semibold">
            <TabLink to="giris" active={tab === "giris"}>
              Giriş yap
            </TabLink>
            <TabLink to="kayit" active={tab === "kayit"}>
              Hesap oluştur
            </TabLink>
          </nav>

          {tab === "giris" ? (
            <>
              {registeredLogin && (
                <p className="mb-4 text-sm text-gold">
                  Hesap oluşturuldu. Şifrenle giriş yapabilirsin.
                </p>
              )}
              <LoginForm key={registeredLogin} defaultLogin={registeredLogin} />
            </>
          ) : (
            <RegisterForm
              turnstileSiteKey={turnstileSiteKey}
              onRegistered={(login) => {
                setRegisteredLogin(login);
                navigate({ search: {} });
              }}
            />
          )}
        </MetinStone>
      </section>
    </main>
  );
}

function TabLink({
  to,
  active,
  children,
}: {
  to: Tab;
  active: boolean;
  children: string;
}) {
  return (
    <Link
      from="/"
      search={to === "kayit" ? { tab: "kayit" } : {}}
      aria-current={active ? "page" : undefined}
      className={`-mb-px border-b-2 pb-3 transition-colors ${active ? "border-gold text-gold" : "border-transparent text-mist hover:text-rice"}`}
    >
      {children}
    </Link>
  );
}

function Ridge() {
  return (
    <svg
      aria-hidden
      viewBox="0 0 1440 320"
      preserveAspectRatio="xMidYMax slice"
      className="pointer-events-none absolute inset-x-0 bottom-0 -z-10 h-[min(38vh,320px)] w-full"
    >
      <path
        fill="#121b3f"
        d="M0 210 L180 120 L300 170 L460 70 L620 190 L760 110 L930 200 L1090 90 L1250 170 L1440 120 V320 H0Z"
      />
      <path
        fill="#0d1534"
        d="M0 260 L220 190 L400 240 L560 170 L760 250 L980 180 L1180 240 L1440 200 V320 H0Z"
      />
    </svg>
  );
}
