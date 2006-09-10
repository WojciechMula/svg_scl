ALL       = 'all'
container = ['svg', 'g', 'defs', 'symbol', 'clipPath', 'mask', 'pattern', 'marker', 'a', 'switch']
graphics  = ['path', 'text', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'image', 'use']
text      = ['text', 'tspan', 'tref', 'textPath']
text2     = text + ['altGlyph']

allowed_tags = {
'alignment-baseline'           : text2,
'baseline-shift'               : text2,
'clip'                         : ['symbol', 'image', 'foreignObject'],
'clip-path'                    : ALL,
'clip-rule'                    : ALL,
#'color'                       : [],
#'color-interpolation'         : [],
#'color-profile'               : [],
#'color-rendering'             : [],
'cursor'                       : container+graphics,
'direction'                    : text,
'display'                      : ALL,
'dominant-baseline'            : text2,
'enable-background'            : container,
'fill'                         : ALL,
'fill-opacity'                 : ALL,
'fill-rule'                    : ALL,
'filter'                       : container + graphics,
'flood-color'                  : ['feFlood'],
'flood-opacity'                : ['feFlood'],
'font'                         : text,
'font-family'                  : text2,
'font-size'                    : text2,
'font-size-adjust'             : ALL,
'font-stretch'                 : text2,
'font-style'                   : text2,
'font-variant'                 : ALL,
'font-weight'                  : text2,
'glyph-orientation-horizontal' : text2,
'glyph-orientation-vertical'   : text2,
'image-rendering'              : ['image'], # only 'image' element?
'kerning'                      : text2,
'letter-spacing'               : text2,
'lighting-color'               : ['feDiffuseLighting', 'feSpecularLighting'],
'marker'                       : ['path', 'line', 'polyline', 'polygon'],
'marker-end'                   : ['path', 'line', 'polyline', 'polygon'],
'marker-mid'                   : ['path', 'line', 'polyline', 'polygon'],
'marker-start'                 : ['path', 'line', 'polyline', 'polygon'],
'mask'                         : ALL,
'opacity'                      : ALL,
'overflow'                     : ['symbol', 'image', 'foreignObject'],
'pointer-events'               : container + graphics,
'shape-rendering'              : ALL,
'stop-color'                   : ['stop'],
'stop-opacity'                 : ['stop'],
'stroke'                       : ALL,
'stroke-dasharray'             : ALL,
'stroke-dashoffset'            : ALL,
'stroke-linecap'               : ALL,
'stroke-linejoin'              : ALL,
'stroke-miterlimit'            : ALL,
'stroke-opacity'               : ALL,
'stroke-width'                 : ALL,
'text-anchor'                  : text2,
'text-decoration'              : text2,
'text-rendering'               : ['text'],
'unicode-bidi'                 : text,
'visibility'                   : ALL,
'word-spacing'                 : text2,
'writing-mode'                 : ['text'],
}

def is_property_allowed(property, tag_name):
	try:
		tags = allowed_tags[property]
		if tags == ALL:
			return True
		else:
			return (tag_name in tags)
	except KeyError:
		return True

def cmp2(a, b):
	return cmp(a,b) == 0

def zero(a, b):
	"""
	Checks if both strings represents number 0; SVG units are recoginzed too.
	
	Regexp: "0\(\.0\*\)\?\(%\|px\|em\|ex\|pt\|pc\|mm\|cm\|in\)\?"
	Sample strings: '0cm', '0.00000', '0.000000in', '0'
	"""
	a = a.replace('.', '0').lstrip('0')
	b = b.replace('.', '0').lstrip('0')
	return (a in ['', '%', 'px', 'em', 'ex', 'pt', 'pc', 'mm', 'cm', 'in']) and \
	       (b in ['', '%', 'px', 'em', 'ex', 'pt', 'pc', 'mm', 'cm', 'in'])

def ints(a, b):
	"""
	Checks if bots strings represents integer values AND
	if these values are equal.

	Regexp: "\([0-9]\+\)\(\.0\*\)?"
	"""
	if a.find('.'):
		a = a.rstrip('0')
		if a[-1] == '.': a = a[:-1]
	if b.find('.'):
		b = b.rstrip('0')
		if b[-1] == '.': b = b[:-1]
	
	try:
		return int(a) == int(b)
	except ValueError:
		return False
	

property_default_values = {
'alignment-baseline'           : (cmp2, None),
'baseline-shift'               : (cmp2, "baseline"),
'clip'                         : (cmp2, "auto"),
'clip-path'                    : (cmp2, "none"),
'clip-rule'                    : (cmp2, "nonzero"),
#'color'                       : (cmp2, None),
#'color-interpolation'         : (cmp2, ""),
#'color-profile'               : (cmp2, ""),
#'color-rendering'             : (cmp2, ""),
'cursor'                       : (cmp2, "auto"),
'direction'                    : (cmp2, "ltr"),
'display'                      : (cmp2, "inline"),
'dominant-baseline'            : (cmp2, "auto"),
'enable-background'            : (cmp2, "accumulate"),
'fill'                         : (cmp2, "black"),
'fill-opacity'                 : (ints, "1"),
'fill-rule'                    : (cmp2, "nonzero"),
'filter'                       : (cmp2, "none"),
'flood-color'                  : (cmp2, "black"),
'flood-opacity'                : (ints, "1"),
'font'                         : (cmp2, None),
'font-family'                  : (cmp2, None),
'font-size'                    : (cmp2, "medium"),
'font-size-adjust'             : (cmp2, "none"),
'font-stretch'                 : (cmp2, "normal"),
'font-style'                   : (cmp2, "normal"),
'font-variant'                 : (cmp2, "normal"),
'font-weight'                  : (cmp2, "normal"),
'glyph-orientation-horizontal' : (zero, "0"),
'glyph-orientation-vertical'   : (cmp2, "auto"),
'image-rendering'              : (cmp2, "auto"),
'kerning'                      : (cmp2, "auto"),
'letter-spacing'               : (cmp2, "normal"),
'lighting-color'               : (cmp2, "white"),
'marker'                       : (cmp2, None),
'marker-end'                   : (cmp2, "none"),
'marker-mid'                   : (cmp2, "none"),
'marker-start'                 : (cmp2, "none"),
'mask'                         : (cmp2, "none"),
'opacity'                      : (ints, "1"),
'overflow'                     : (cmp2, None),
'pointer-events'               : (cmp2, "visiblePainted"),
'shape-rendering'              : (cmp2, "auto"),
'stop-color'                   : (cmp2, "black"),
'stop-opacity'                 : (ints, "1"),
'stroke'                       : (cmp2, "none"),
'stroke-dasharray'             : (cmp2, "none"),
'stroke-dashoffset'            : (zero, "0"),
'stroke-linecap'               : (cmp2, "butt"),
'stroke-linejoin'              : (cmp2, "miter"),
'stroke-miterlimit'            : (ints, "4"),
'stroke-opacity'               : (ints, "1"),
'stroke-width'                 : (ints, "1"),
'text-anchor'                  : (cmp2, "start"),
'text-decoration'              : (cmp2, "none"),
'text-rendering'               : (cmp2, "auto"),
'unicode-bidi'                 : (cmp2, "normal"),
'visibility'                   : (cmp2, "inherit"),
'word-spacing'                 : (cmp2, "normal"),
'writing-mode'                 : (cmp2, "lr-tb"),
}

SVG_properties = property_inherits = {
'alignment-baseline'           : False,
'baseline-shift'               : False,
'clip'                         : False,
'clip-path'                    : False,
'clip-rule'                    : True,
'color'                        : False, # !!!
'color-interpolation'          : True,
'color-profile'                : True,
'color-rendering'              : True,
'cursor'                       : True,
'direction'                    : True,
'display'                      : False, # !!!
'dominant-baseline'            : False,
'enable-background'            : False,
'fill'                         : False,
'fill-opacity'                 : True,
'fill-rule'                    : True,
'filter'                       : False,
'flood-color'                  : False,
'flood-opacity'                : False,
'font'                         : True,
'font-family'                  : True,
'font-size'                    : False, # !!!
'font-size-adjust'             : True,
'font-stretch'                 : True,
'font-style'                   : True,
'font-variant'                 : True,
'font-weight'                  : True,
'glyph-orientation-horizontal' : True,
'glyph-orientation-vertical'   : True,
'image-rendering'              : True,
'kerning'                      : True,
'letter-spacing'               : True,
'lighting-color'               : False,
'marker'                       : False, # !!!
'marker-end'                   : False, # !!!
'marker-mid'                   : False, # !!!
'marker-start'                 : False, # !!!
'mask'                         : False,
'opacity'                      : False,
'overflow'                     : False,
'pointer-events'               : True,
'shape-rendering'              : True,
'stop-color'                   : False,
'stop-opacity'                 : False,
'stroke'                       : False, # !!!
'stroke-dasharray'             : True,
'stroke-dashoffset'            : True,
'stroke-linecap'               : True,
'stroke-linejoin'              : True,
'stroke-miterlimit'            : True,
'stroke-opacity'               : True,
'stroke-width'                 : True,
'text-anchor'                  : True,
'text-decoration'              : False,
'text-rendering'               : True,
'unicode-bidi'                 : False,
'visibility'                   : False,
'word-spacing'                 : True,
'writing-mode'                 : True,
}


def warning(s):
	print >> stderr, "Warning:", s
	pass

def style2dict(style):
	dict  = {}
	style = style.strip()
	if style == '':
		return dict
	
	for item in style.split(';'):
		pv = item.split(':', 2)
		if len(pv) == 1:
				property = pv[0].strip()
				value     = "0"
				warning("property or value missing '%s', transformed into '%s:0'" % (pv, pv))
		else:
				property = pv[0].strip()
				value    = pv[1].strip()

		if property == '':
			warning("property with no name! (value is '%s') - removing" % value)
		elif value == '':
			warning("property with no value! (name is '%s') - removing" % value)
		else:
			dict[property] = value
	#rof
	return dict

def dict2style(dict):
	return ";".join(["%s:%s" % item for item in dict.iteritems()])

def inherited_style(style, inherited):
	iherited2 = inherited.copy()
	
	if len(style) == 0:
		return inherited2

	for property, value in style.iteritems():
		if property not in SVG_properties:
			continue	# don't touch unknown properties

		if property in property_inherits:
			if property_inherits[property] == True:
				inherits2[property] = value
	
	return inherited2

def simplify_style(element, old_style, inherited):
	
	new_style = old_style.copy()

	for property, value in old_style.iteritems():
		if property not in SVG_properties:
			continue	# don't touch unknown properties

		if not is_property_allowed(property, element.nodeName):
			# porperty not allowed for this tag
			new_style.pop(property);
			warning("property '%s' does not apply to the tag '%s' - removing" % (property, element.nodeName))
			continue

		if property in property_inherits and property_inherits[property]:
			try:
				if value == inherited[property]:
					new_style.pop(property)
					warning("property '%s' has the same value ('%s') as inherited -- removing" % (property, value))
					continue
			except KeyError:
				pass

		if property in property_default_values:
			cmpfun, default = property_default_values[property]
			if cmpfun(value, default):
				new_style.pop(property)
				warning("property '%s' has default value '%s' - removing" % (property, value))
				continue
	
	return new_style
#fed

def clean(root, inherited={}):
	for element in root.childNodes:
		if element.nodeType != element.ELEMENT_NODE:
			continue

		if not element.hasAttribute("style"):
			if element.nodeName in container:
				clean(element, inherited)
		else:
			style1 = style2dict(element.getAttribute("style"))
			style2 = simplify_style(element, style1, inherited)
			if len(style1) != len(style2):
				if len(style2) > 0:
					element.setAttribute("style", dict2style(style2))
				else:
					element.removeAttribute("style");
		
			if element.nodeName in container:
				if len(style2) > 0:
					inherited = inherited_style(style2, inherited)
				clean(element, inherited);
	#rof
#fed

from sys import argv, stderr, stdout
from xml.dom.minidom import parse
import xml.dom as DOM

document = parse(argv[1])
drawing = document.getElementsByTagName('svg')[0]

clean(drawing)
print document.toxml().encode(document.encoding)

# vim: ts=4 sw=4
