def generer_decision(kpi_df):
    def decide(row):
        stock = row["Stock_Actuel"]
        couverture = row["Jours_Couverture"]
        cible = row["Stock_Cible"]

        if stock < 0:
            return "❌ Rupture de stock ! Agir immédiatement"
        elif couverture < 15:
            return "⚠️ Stock faible : Commander vite"
        elif stock > 2 * cible:
            return "📦 Surstock ! Réduire les commandes"
        elif stock > cible:
            return "✅ Stock suffisant, pas d'action"
        else:
            return "🔍 Surveiller la consommation"

    decisions = kpi_df[["Article", "Stock_Actuel", "Jours_Couverture", "Stock_Cible"]].copy()
    decisions["Décision"] = decisions.apply(decide, axis=1)
    return decisions[["Article", "Stock_Actuel", "Jours_Couverture", "Stock_Cible", "Décision"]]
