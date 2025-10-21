import { Outfit } from "../types/plan";
export default function OutfitCard({ outfit }:{ outfit: Outfit }) {
  return (
    <section style={{ border: "1px solid #eee", borderRadius: 8, padding: 12 }}>
      <h3>Preporuka za odjeću</h3>
      <ul>
        <li>Gore: {outfit.top}</li>
        <li>Dolje: {outfit.bottom}</li>
        <li>Jakna: {outfit.outerwear}</li>
        <li>Obuća: {outfit.shoes}</li>
        {!!outfit.accessories?.length && <li>Dodaci: {outfit.accessories.join(", ")}</li>}
      </ul>
    </section>
  );
}
