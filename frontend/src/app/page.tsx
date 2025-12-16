export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-void p-8">
      <div className="text-center">
        <h1 className="font-serif text-5xl font-bold text-gold">Alembic</h1>
        <p className="mt-4 text-lg text-silver">
          The Hermetic Tarot Mirror
        </p>
        <p className="mt-6 max-w-2xl text-cream">
          Transform questions into insight through the ancient wisdom of tarot.
          A vessel of transformation where synchronicity meets intelligence.
        </p>
        <div className="mt-12 flex gap-4 justify-center">
          <button className="rounded-lg bg-gold px-8 py-3 font-medium text-void hover:bg-cream transition-colors">
            Begin Reading
          </button>
          <button className="rounded-lg border border-gold px-8 py-3 font-medium text-gold hover:bg-gold hover:text-void transition-colors">
            Learn More
          </button>
        </div>
      </div>
    </main>
  );
}
