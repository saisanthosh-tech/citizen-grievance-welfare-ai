"""
Test script to verify Telugu and Tamil translations are complete
"""

from translations import TRANSLATIONS

# Check all languages have the same keys
en_keys = set(TRANSLATIONS['en'].keys())
hi_keys = set(TRANSLATIONS['hi'].keys())
te_keys = set(TRANSLATIONS['te'].keys())
ta_keys = set(TRANSLATIONS['ta'].keys())

print("=" * 60)
print("TRANSLATION COMPLETENESS CHECK")
print("=" * 60)
print(f'\n✓ English keys: {len(en_keys)}')
print(f'✓ Hindi keys: {len(hi_keys)}')
print(f'✓ Telugu keys: {len(te_keys)}')
print(f'✓ Tamil keys: {len(ta_keys)}')

# Check for missing keys
missing_te = en_keys - te_keys
missing_ta = en_keys - ta_keys
extra_te = te_keys - en_keys
extra_ta = ta_keys - en_keys

print("\n" + "=" * 60)
print("MISSING KEYS CHECK")
print("=" * 60)

if missing_te:
    print(f'\n❌ Missing Telugu keys ({len(missing_te)}):')
    for key in sorted(missing_te):
        print(f'   - {key}')
else:
    print('\n✅ Telugu: All keys present!')

if missing_ta:
    print(f'\n❌ Missing Tamil keys ({len(missing_ta)}):')
    for key in sorted(missing_ta):
        print(f'   - {key}')
else:
    print('\n✅ Tamil: All keys present!')

if extra_te:
    print(f'\n⚠️  Extra Telugu keys ({len(extra_te)}):')
    for key in sorted(extra_te):
        print(f'   - {key}')

if extra_ta:
    print(f'\n⚠️  Extra Tamil keys ({len(extra_ta)}):')
    for key in sorted(extra_ta):
        print(f'   - {key}')

print("\n" + "=" * 60)
print("SAMPLE TRANSLATIONS")
print("=" * 60)

# Test some key translations
test_keys = ['app_title', 'submit_grievance', 'track_grievance', 'healthcare', 'education']

for key in test_keys:
    print(f'\n{key}:')
    print(f'  EN: {TRANSLATIONS["en"].get(key, "MISSING")}')
    print(f'  HI: {TRANSLATIONS["hi"].get(key, "MISSING")}')
    print(f'  TE: {TRANSLATIONS["te"].get(key, "MISSING")}')
    print(f'  TA: {TRANSLATIONS["ta"].get(key, "MISSING")}')

print("\n" + "=" * 60)
print("FINAL RESULT")
print("=" * 60)

if not missing_te and not missing_ta:
    print('\n✅ ✅ ✅ ALL TRANSLATIONS COMPLETE! ✅ ✅ ✅')
    print('\nYou can now use all 4 languages:')
    print('  - English (en)')
    print('  - Hindi (hi)')
    print('  - Telugu (te)')
    print('  - Tamil (ta)')
else:
    print('\n❌ Some translations are missing. Please review above.')

print("\n" + "=" * 60)
