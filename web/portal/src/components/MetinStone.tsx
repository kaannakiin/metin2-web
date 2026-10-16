import type { ReactNode } from "react";

// A Metin stone: the gold rim is the outer shape showing 1.5px around the
// inner one; the aura sits on a wrapper because drop-shadow follows clip-path.
export function MetinStone({ children }: { children: ReactNode }) {
  return (
    <div className="animate-stone-land">
      <div className="animate-aura">
        <div className="bg-linear-to-b from-gold/80 via-gold/30 to-gold/60 p-[1.5px] stone-shape">
          <div className="bg-[linear-gradient(118deg,transparent_38%,rgb(237_230_214/0.035)_38%,transparent_72%),radial-gradient(120%_80%_at_30%_0%,#232d63_0%,#121a3d_45%,#0a1028_100%)] px-9 pt-14 pb-10 stone-shape sm:px-12">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
