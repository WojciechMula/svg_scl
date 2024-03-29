# -*- coding: iso-8859-2 -*-

__README__ = """
===========================================================
                  SVG style cleanup
===========================================================


Introduction
------------------------------------------------------------

This program cleans **inline** style definition, removing
properties that are not necessary to proper render image.

1. Some properties don't apply to all SVG_ tags --- for
   example markers ("arrows") applies only to paths.
   And such properties could be removed if present in
   style of other elements.

   Enabled with option ``-a``

2. Some properties has the same value as property of parent
   node.  If a property inherits than setting it again in a
   child node isn't needed.  For example::

	   <svg ...>
	   <g style="stroke-width: 2px">
		  <line style="stroke-width: 2px" x1=.../>
		  <line style="stroke-width: 3px" x1=.../>
		  <line style="stroke-width: 2px" x1=.../>
		  <line style="stroke-width: 2px" x1=.../>
	   </g>
	   </svg>

   After transformation::
  
	   <svg ...>
	   <g style="stroke-width: 2px">
		  <line x1=.../>
		  <line style="stroke-width: 3px" x1=.../>
		  <line x1=.../>
		  <line x1=.../>
	   </g>
	   </svg>
   
   Enabled with option ``-i``

3. Properties that has default value are removed too.
   
   Enabled with option ``-i``


Since program doesn't know anything about CSS, methods 2
and 3 could be safety used with files not using local
or external stylesheets.


Author
-----------------------------------------------------------

Wojciech Mu�a, wojciech_mula@poczta.onet.pl
BSD license


.. _SVG:		http://www.w3.org/TR/SVG/
.. _Inkscape:	http://www.inkscape.org/
"""



#######################################################################

def property_applies(property, tag_name):
	"""
	Returns true if for a property applies to the tag.

	For example 'writing-mode' applies to just one tag ('text'),
	'display' applies to all SVG tags.
	"""
	try:
		tags = allowed_tags[property]
		if tags == ALL:
			return True
		else:
			return (tag_name in tags)
	except KeyError:
		return True

# tags name
ALL       = 'all'	# special value
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

#######################################################################

def has_default_value(property, value):
	try:
		cmpfun, default = property_default_value[property]
		return cmpfun(value, default)
	except KeyError:
		return False

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
	Checks if both strings represents integer values AND
	if these values are equal.

	Regexp: "\([0-9]\+\)\(\.0\*\)?"
	"""
	if a.find('.') >= 0:
		a = a.rstrip('0')
		if a[-1] == '.': a = a[:-1]
	if b.find('.') >= 0:
		b = b.rstrip('0')
		if b[-1] == '.': b = b[:-1]
	
	try:
		return int(a) == int(b)
	except ValueError:
		return False
	

property_default_value = {
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

#######################################################################

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


def echo(s):
	if not options.quiet:
		print >> sys.stderr, s

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
				echo("property or value missing '%s', transformed into '%s:0'" % (pv, pv))
		else:
				property = pv[0].strip()
				value    = pv[1].strip()

		if property == '':
			echo("property with no name! (value is '%s') - removed" % value)
		elif value == '':
			echo("property with no value! (name is '%s') - removed" % value)
		else:
			dict[property] = value
	#rof
	return dict

def dict2style(dict):
	return ";".join(["%s:%s" % item for item in dict.iteritems()])

def inherited_style(style, inherited):
	inherited2 = inherited.copy()
	
	if len(style) == 0:
		return inherited2

	for property, value in style.iteritems():
		if property not in SVG_properties:
			continue	# don't touch unknown properties

		if property in property_inherits:
			if property_inherits[property] == True:
				inherited2[property] = value
	
	return inherited2

def simplify_style(element, old_style, inherited):
	
	new_style = old_style.copy()

	for property, value in old_style.iteritems():
		if property not in SVG_properties:
			continue	# don't touch unknown properties

		if not property_applies(property, element.nodeName) and options.a:
			# porperty not applies to this tag
			new_style.pop(property);
			echo("property '%s' does not apply to the tag '%s' - removed" % (property, element.nodeName))
			continue

		if not options.i: # do not apply inheritence
			continue

		if property in property_inherits and property_inherits[property]:
			try:
				if value == inherited[property]:
					new_style.pop(property)
					echo("property '%s' has the same value ('%s') as inherited -- removed" % (property, value))
					continue
			except KeyError:
				pass

		if property in property_default_value:
			cmpfun, default = property_default_value[property]
			if cmpfun(value, default):
				new_style.pop(property)
				echo("property '%s' has default value '%s' - removed" % (property, value))
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


#######################################################################

if __name__ == '__main__':
	import optparse
	import os
	import sys

	parser = optparse.OptionParser()
	parser.add_option('-f', '--file', dest='filename', 
	                   help="SVG file name", metavar="FILE")
	parser.add_option('-q', '--quiet', action="store_true", dest='quiet', default=False,
	                   help="do not print on stderr any messages")
	parser.add_option('-p', '--pretty-print', action="store_true", dest='pretty', default=False,
	                  help="pretty print SVG")
	parser.add_option('-a', action="store_true", dest='a', default=False,
	                  help="remove properties that not apply to certain SVG tag")
	parser.add_option('-i', action="store_true", dest='i', default=False,
	                  help="remove properties that have some value as parent's property or have default values")
	parser.add_option('-r', '--readme', action="store_true", dest="print_readme", default=False,
	                  help="print README - more details and examples")

	(options, args) = parser.parse_args()
	if options.print_readme:
		print __README__
		sys.exit()
	
	if not options.filename:
		parser.print_help()
		sys.exit()

	import xml.dom.minidom

	if not os.path.isfile(options.filename):
		sys.exit()

	document = xml.dom.minidom.parse(options.filename)
	svg = document.getElementsByTagName('svg')
	assert len(svg) == 1 # only one <svg> tag allowed
	svg = svg[0]

	if options.a or options.i:
		clean(svg)

	if options.pretty:
		if document.encoding:
			print document.toprettyxml().encode(document.encoding)
		else:
			print document.toprettyxml()
	else:
		if document.encoding:
			print document.toxml().encode(document.encoding)
		else:
			print document.toxml()
	sys.exit()

# vim: ts=4 sw=4
